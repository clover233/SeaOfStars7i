"""优酷动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class YoukuCase(WdaCase):
    PACKAGE = 'com.youku.YouKu'
    APP_NAME = '优酷'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
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
            logging.exception('设置优酷 WDA 连续页面模式失败')
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束优酷进程失败，继续启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            settings = getattr(self, '_previous_idle_settings', None)
            if settings is not None:
                try:
                    self.device.appium_settings(settings)
                except Exception:
                    logging.exception('恢复 WDA idle 设置失败')
            self._previous_idle_settings = None

    def dismiss_startup_prompts(self):
        for _ in range(7):
            nodes = self.nodes()
            button = self.find(
                '同意并继续', '同意', '要求 App 不跟踪',
                '以后再说', '暂不开启', '暂不更新', '我知道了',
                '跳过', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def edge_back(self, wait=3):
        back = self.find('返回', contains=True, max_y=150)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(4, 437, 350, 437, 0.3)
        time.sleep(wait)

    def return_youku_home(self):
        for _ in range(10):
            nodes = self.nodes()
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                if any(node.tag == 'XCUIElementTypeSearchField'
                       and node.get('visible') == 'true' for node in self.nodes()):
                    return
                continue
            cancel = self.find('取消', max_y=140, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(3)
                continue
            self.edge_back(wait=3)
        self.fail('多次返回后仍未到达优酷首页')

    def start_youku(self):
        self.start_app(wait=0)

    def finish_youku_start(self):
        self.dismiss_startup_prompts()
        self.return_youku_home()

    def select_channel(self, name):
        self.tap(name, max_y=155, wait=5)

    def open_search(self):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeSearchField']
        if not fields:
            self.fail('优酷首页未找到搜索框')
        self.tap_node(fields[0])
        time.sleep(2)

    def input_search(self, query):
        self.enter_text(query, clear=True)

    def submit_search(self):
        self.tap('Search', '搜索', min_y=700, wait=7)

    def repeat_search(self, query):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeSearchField']
        if not fields:
            self.fail('搜索结果页未找到搜索框')
        self.tap_node(fields[0])
        time.sleep(2)
        self.enter_text(query, clear=True)
        self.submit_search()

    def play_dahuatextian(self, seconds=30):
        play = self.find('免费试看', '立即播放', min_y=400)
        if play is None:
            self.fail('“大话天仙”搜索结果没有可用的播放入口')
        self.tap_node(play)
        time.sleep(7)
        if self.find('返回', max_y=150) is None:
            self.fail('点击播放后未进入视频详情页')
        time.sleep(seconds)
