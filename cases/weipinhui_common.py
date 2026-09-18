"""唯品会动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class WeipinhuiCase(WdaCase):
    PACKAGE = 'com.vipshop.iphone'
    APP_NAME = '唯品会'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾步骤的 trace 采样窗口不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        self._previous_idle_settings = None
        try:
            settings = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': settings.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': settings.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置唯品会连续页面模式失败')

    def _restore_idle_settings(self):
        settings = getattr(self, '_previous_idle_settings', None)
        if settings is not None:
            try:
                self.device.appium_settings(settings)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束唯品会进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭广告、升级和权限说明；系统权限弹窗优先拒绝。"""
        for _ in range(8):
            try:
                alert = self.device.alert
                buttons = alert.buttons()
                if buttons:
                    if '不允许' in buttons:
                        alert.click('不允许')
                    elif '取消' in buttons:
                        alert.click('取消')
                    else:
                        alert.dismiss()
                    time.sleep(2)
                    continue
            except Exception:
                pass
            nodes = self.nodes()
            button = self.find(
                '关闭', '以后再说', '暂不升级', '暂不开启', '稍后再说',
                '我知道了', '跳过', '取消', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def _is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.find('已选中首页', min_y=760, nodes=nodes) is not None
                or (self.find('首页', min_y=760, nodes=nodes) is not None
                    and self.find('收藏', min_y=760, nodes=nodes) is not None))

    def return_home(self):
        for _ in range(10):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self._is_home(nodes):
                return
            home = self.find('首页', '已选中首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                continue
            back = self.find('返回按钮', '返回', max_y=150, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
            time.sleep(3)
        self.fail('多次返回后仍未到达唯品会首页')

    def start_weipinhui(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()
        if self.find('登录', '登录/注册', contains=True) is not None:
            self.fail('唯品会未登录，请先预置已登录账号')

    def search_product(self, query):
        nodes = self.nodes()
        search = next((node for node in nodes
                       if node.get('visible') == 'true'
                       and float(node.get('y', 999)) < 180
                       and ('搜索' in self.node_name(node))), None)
        if search is None:
            self.fail('唯品会首页未找到搜索框')
        self.tap_node(search)
        time.sleep(3)
        self.enter_text(query, clear=True)
        self.tap('搜索', max_y=180, wait=7)
        if self.find(query, contains=True) is None:
            # 结果卡片文案会随活动变化，至少要求离开搜索输入页并出现商品节点。
            products = self._product_nodes()
            if not products:
                self.fail('搜索后没有出现“{}”商品结果'.format(query))

    def _product_nodes(self):
        return sorted([
            node for node in self.nodes()
            if node.get('visible') == 'true'
            and 160 <= float(node.get('y', 0)) < 760
            and '商品' in self.node_name(node)
        ], key=lambda node: (float(node.get('y', 0)), float(node.get('x', 0))))

    def open_first_product(self):
        products = self._product_nodes()
        if not products:
            self.fail('搜索结果页没有可打开的商品')
        self.tap_node(products[0])
        time.sleep(7)
        if self.find('店铺按钮', '购买按钮', contains=True) is None:
            self.fail('点击第一条商品后未进入商品详情')

    def open_store(self):
        self.tap('店铺按钮', '进店逛逛', '进入店铺', contains=True, wait=7)

    def return_product_detail(self):
        self.tap('返回按钮', '返回', max_y=160, wait=5)
        if self.find('购买按钮', contains=True) is None:
            self.fail('返回后未到商品详情页')

    def add_to_cart(self):
        """当前版本购买栏的右半区是加入购物车，控件本身覆盖整个价格栏。"""
        button = self.find('购买按钮', contains=True)
        if button is None:
            self.fail('商品详情页未找到购买栏')
        x = round(float(button.get('x', 0)) + float(button.get('width', 0)) * 0.82)
        y = round(float(button.get('y', 0)) + float(button.get('height', 0)) / 2)
        self.device.click(x, y)
        time.sleep(4)
        self.dismiss_optional_prompts()

    def open_cart(self):
        self.tap('购物车按钮', '购物车', contains=True, wait=6)
        if self.find('结算', contains=True) is None:
            self.fail('点击购物车后未进入购物车页')

    def open_checkout(self):
        self.tap('结算', contains=True, wait=6)
        self.dismiss_optional_prompts()
        # 只进入确认/结算页，绝不点击提交订单或支付。
        if self.find('提交订单', '确认订单', '收银台', contains=True) is None:
            logging.warning('结算页标题不可访问，将按返回控件确认页面切换')

    def return_to_cart(self):
        nodes = self.nodes()
        close = self.find('关闭', max_y=160, nodes=nodes)
        back = self.find('返回按钮', '返回', max_y=160, nodes=nodes)
        if close is not None:
            self.tap_node(close)
        elif back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
        time.sleep(5)
        if self.find('结算', contains=True) is None:
            self.fail('从结算页返回后未到购物车')

    def long_press_top_cart_item(self):
        """按表格长按顶部商品；当前版本不响应时降级为左滑。"""
        self.device.tap_hold(200, 430, 1.5)
        time.sleep(3)
        if self.find('删除', contains=True) is None:
            self.device.swipe(0.82, 0.43, 0.30, 0.43, 0.35)
            time.sleep(3)

    def delete_revealed_cart_item(self):
        delete = self.find('删除', contains=True)
        if delete is None:
            self.fail('长按和左滑商品后均未出现删除按钮')
        self.tap_node(delete)
        time.sleep(3)
        confirm = self.find('删除', '确定', contains=True, max_y=700)
        if confirm is not None:
            self.tap_node(confirm)
            time.sleep(4)

    def open_sport(self):
        self.tap('运动', max_y=220, wait=7)

    def open_outlet_equivalent(self):
        """旧版“唯品奥莱”已下线；优先原入口，否则进入“天天低价”。"""
        outlet = self.find('唯品奥莱', contains=True)
        if outlet is not None:
            self.tap_node(outlet)
            time.sleep(7)
            return
        # 新版运动频道中没有奥莱底栏，先回首页再走分类页的等价入口。
        self.return_home()
        more = self.find('更多按钮', '更多', max_y=220, contains=True)
        if more is None:
            self.fail('当前版本没有“唯品奥莱”，也未找到“更多”分类入口')
        self.tap_node(more)
        time.sleep(5)
        low_price = self.find('天天低价', contains=True)
        if low_price is None:
            self.fail('“唯品奥莱”已下线，分类页也没有可替代的“天天低价”')
        self.tap_node(low_price)
        time.sleep(7)
