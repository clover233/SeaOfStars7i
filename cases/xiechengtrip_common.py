"""携程旅行 iOS 动态性能用例公共能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class XiechengTripCase(WdaCase):
    PACKAGE = 'ctrip.com'
    APP_NAME = '携程旅行'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只采集首尾步骤，并保证每个采样窗口不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
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
            logging.exception('设置携程连续页面模式失败')

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
            logging.exception('结束携程旅行进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭不影响业务的广告、更新、跟踪及民宿问卷。"""
        for _ in range(5):
            nodes = self.nodes()
            survey = self.find('后续出行时', contains=True, nodes=nodes)
            if survey is not None:
                # 问卷关闭图标没有可读名称，位置固定在问卷卡片右上角。
                y = round(float(survey.get('y', 360)) + 13)
                self.device.click(377, y)
                time.sleep(1)
                continue
            button = self.find(
                '要求App不跟踪', '要求 App 不跟踪', '不允许', '以后再说',
                '下次再说', '暂不开启', '暂不更新', '我知道了', '取消',
                '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=220, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        home = self.find('首页', min_y=730, nodes=nodes)
        features = any(self.find(name, max_y=620, nodes=nodes) is not None
                       for name in ('机票', '火车票', '民宿/客栈'))
        return home is not None and features

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_home(nodes):
                return
            home = self.find('首页', min_y=730, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                continue
            back = self.find('返回', max_y=150, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.90, 0.5, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达携程旅行主界面')

    def start_xiecheng(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()

    def open_home_feature(self, name, fallback):
        self.tap(name, fallback=fallback, wait=6, timeout=4)
        self.dismiss_optional_prompts()

    def open_homestay(self):
        self.open_home_feature('民宿/客栈', (326, 340))

    def query_homestay(self):
        self.tap('查询', fallback=(201, 438), contains=True,
                 min_y=300, max_y=650, choose='last', wait=6)

    def search_homestay(self, keyword):
        self.tap('位置/民宿名/编号', '位置/民宿名/关键词',
                 fallback=(205, 84), contains=True, max_y=180, wait=1)
        self.enter_text(keyword)
        self.tap('Search', '搜索', fallback=(355, 825),
                 min_y=720, choose='last', wait=8)

    def open_first_homestay(self):
        candidates = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and self.node_name(node).startswith('1 /')
                      and float(node.get('y', 0)) > 180]
        if candidates:
            self.tap_node(sorted(candidates,
                                 key=lambda n: float(n.get('y', 0)))[0])
        else:
            self.device.click(201, 360)
        time.sleep(8)

    def open_reviews(self):
        self.dismiss_optional_prompts()
        self.tap('评价', max_y=180, wait=4)

    def open_all_reviews(self):
        self.dismiss_optional_prompts()
        matches = [node for node in self.nodes()
                   if node.get('visible') == 'true'
                   and self.node_name(node).startswith('全部')
                   and self.node_name(node).endswith('条')
                   and float(node.get('y', 0)) > 180]
        if not matches:
            self.fail('未找到动态评论总数入口')
        self.tap_node(sorted(matches, key=lambda n: float(n.get('y', 0)))[0])
        time.sleep(6)

    def edge_back(self, wait=4):
        self.device.swipe(0.01, 0.5, 0.90, 0.5, 0.3)
        time.sleep(wait)

    def open_all_facilities(self):
        self.dismiss_optional_prompts()
        self.tap('设施', max_y=180, wait=4)
        self.tap('全部设施', fallback=(342, 448), contains=True,
                 min_y=180, timeout=5, wait=4)

    def close_facilities(self):
        nodes = self.nodes()
        close = self.find('关闭', 'close', max_y=300, nodes=nodes)
        if close is not None:
            self.tap_node(close)
        else:
            title = self.find('全部设施', contains=True, max_y=350, nodes=nodes)
            y = 90 if title is None else max(
                75, round(float(title.get('y', 75)) + 15))
            self.device.click(376, y)
        time.sleep(3)

    def open_flight(self):
        self.open_home_feature('机票', (120, 257))

    def query_flight(self):
        self.tap('查询', '搜索', '查机票', fallback=(201, 528),
                 contains=True, min_y=280, max_y=700, wait=10)
        self._fail_on_empty_result('机票')

    def open_first_flight(self):
        self.device.click(205, 245)
        time.sleep(8)

    def open_train(self):
        self.open_home_feature('火车票', (201, 257))

    def query_train(self):
        self.tap('查询', '搜索', '查询车票', fallback=(201, 528),
                 contains=True, min_y=280, max_y=700, wait=12)
        self._fail_on_empty_result('火车票')

    def open_first_train(self):
        self.device.click(205, 245)
        time.sleep(7)

    def book_first_train(self):
        self.tap('预订', '订', fallback=(354, 305),
                 min_y=150, max_y=760, wait=7)

    def _fail_on_empty_result(self, scene):
        nodes = self.nodes()
        if any(self.find(text, contains=True, nodes=nodes) is not None
               for text in ('暂无结果', '暂无符合', '未查询到')):
            self.fail('当前预置的{}线路或日期没有可浏览结果'.format(scene))
