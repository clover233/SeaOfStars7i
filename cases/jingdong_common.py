"""京东动态性能用例的 WDA 页面能力。"""
import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class JingdongCase(WdaCase):
    PACKAGE = 'com.360buy.jdmobile'
    APP_NAME = '京东'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        """直播和商品详情持续动画时不等待 XCTest idle。"""
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get('animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置 WDA 连续页面模式失败')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is not None:
            try:
                self.device.appium_settings(previous)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束京东进程失败，继续启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        for _ in range(5):
            nodes = self.nodes()
            if self.find('领取并使用', nodes=nodes) is not None:
                self.device.click(201, 605)  # 直播券浮层的无名关闭按钮
                time.sleep(2)
                continue
            button = self.find('不允许', '以后再说', '我知道了', '暂不',
                               '取消', 'pd recommend pop close', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def fail_if_security_verification(self):
        nodes = self.nodes()
        if (self.find('安全验证', nodes=nodes) is not None or
                self.find('请按照图中轨迹绘制', contains=True,
                          nodes=nodes) is not None):
            self.fail('触发京东安全验证，请先人工完成验证再运行')

    def start_jingdong(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_home()

    def edge_back(self, wait=3):
        nodes = self.nodes()
        back = self.find('返回', 'Return', 'MenuIconBack White',
                         max_y=150, nodes=nodes)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_home(self):
        for _ in range(14):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            home = self.find('首页', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                return
            close = self.find('关闭', 'close', max_y=760, nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(2)
            else:
                self.edge_back(wait=2)
        self.fail('多次返回后仍未到达京东首页')

    def top_entry(self, name, fallback=None, wait=5):
        self.tap(name, max_y=260, fallback=fallback, wait=wait)

    def bottom_tab(self, name, wait=4):
        self.tap(name, min_y=740, wait=wait)

    def open_category(self):
        # 当前版本入口在首页顶部右侧，不在底部。
        self.tap('分类', max_y=220, fallback=(363, 147), wait=4)

    def open_computer_category(self):
        computer = self.find('电脑', '电脑办公', contains=True)
        if computer is not None:
            self.tap_node(computer)
            time.sleep(4)
            return
        # 分类页为 Canvas；回到 3C 页进入同一个电脑分类。
        self.edge_back()
        self.return_home()
        self.top_entry('手机数码', fallback=(82, 230), wait=4)
        self.tap('电脑', max_y=260, fallback=(170, 168), wait=4)

    def tap_first_category_product(self):
        nodes = self.nodes()
        candidates = [n for n in nodes if n.get('visible') == 'true'
                      and n.tag in ('XCUIElementTypeImage', 'XCUIElementTypeOther')
                      and 180 <= float(n.get('y', 0)) <= 700
                      and float(n.get('width', 0)) >= 60]
        if candidates:
            self.tap_node(sorted(candidates, key=lambda n: float(n.get('y', 0)))[0])
        else:
            self.device.click(155, 320)
        time.sleep(5)

    def open_search(self):
        self.device.click(190, 116)
        time.sleep(3)

    def submit_search(self, text):
        self.enter_text(text, clear=True)
        self.tap('搜索', max_y=180, fallback=(362, 116), wait=5)
        self.fail_if_security_verification()

    def open_first_search_result(self):
        nodes = self.nodes()
        results = [n for n in nodes if n.get('visible') == 'true'
                   and n.tag == 'XCUIElementTypeOther'
                   and 480 <= float(n.get('y', 0)) <= 780
                   and float(n.get('height', 0)) >= 100]
        if results:
            self.tap_node(sorted(results, key=lambda n: float(n.get('y', 0)))[0])
        else:
            self.device.click(110, 585)
        time.sleep(6)

    def open_reviews_section(self):
        for _ in range(6):
            review = self.find('买家评价', '评价', contains=True)
            if review is not None:
                self.tap_node(review)
                time.sleep(3)
                return
            self.device.swipe(0.5, 0.75, 0.5, 0.32, 0.3)
            time.sleep(1)

    def open_all_reviews(self):
        self.tap('全部评价', '查看全部评价', contains=True,
                 fallback=(325, 130), wait=4)

    def open_purchase(self):
        self.tap('立即购买', '购买', contains=True,
                 fallback=(337, 812), wait=4)

    def confirm_purchase(self):
        confirm = self.find('确认', '确定', '选好了')
        if confirm is not None:
            self.tap_node(confirm)
            time.sleep(4)

    def open_seconds(self):
        self.tap('秒送', max_y=120, fallback=(150, 54), wait=5)

    def open_takeout(self):
        self.tap('外卖', max_y=320, fallback=(48, 190), wait=5)

    def open_first_merchant(self):
        self.device.click(200, 405)
        time.sleep(5)

    def add_first_merchant_item(self):
        self.device.click(378, 458)
        time.sleep(2)

    def open_merchant_cart(self):
        self.device.click(34, 805)
        time.sleep(2)

    def checkout_merchant(self):
        self.device.click(340, 808)
        time.sleep(5)

    def open_supermarket(self):
        self.top_entry('京东超市', fallback=(127, 230), wait=5)

    def open_grocery(self):
        self.tap('粮油调味', fallback=(182, 212), wait=5)
        self.fail_if_security_verification()

    def add_first_grocery_item(self):
        self.device.click(371, 421)  # H5 加号，402x874 WEditor 坐标
        time.sleep(3)

    def checkout_visible_cart(self):
        self.tap('去结算', '结算', contains=True,
                 fallback=(334, 810), wait=5)

    def open_live_list(self):
        self.bottom_tab('逛')
        self.tap('直播', max_y=180, fallback=(315, 105), wait=6)

    def open_first_live(self):
        self.device.click(100, 400)
        time.sleep(7)
        self.dismiss_optional_prompts()

    def focus_live_comment(self):
        for _ in range(3):
            self.dismiss_optional_prompts()
            chat = self.find('聊天框', '说点什么', contains=True)
            if chat is not None:
                self.tap_node(chat)
            else:
                self.device.click(130, 811)
            time.sleep(2)
            fields = [n for n in self.nodes()
                      if n.tag in ('XCUIElementTypeTextField', 'XCUIElementTypeTextView')
                      and n.get('visible') == 'true']
            if fields:
                return
        self.fail('直播聊天框被活动浮层遮挡')

    def send_live_comment(self, text):
        self.enter_text(text)
        self.tap('发送', fallback=(360, 760), wait=3)

    def open_live_bag(self):
        self.tap('购物袋', contains=True, fallback=(365, 790), wait=4)
