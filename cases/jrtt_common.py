"""今日头条动态性能用例的 WDA 页面能力。"""
import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class JrttCase(WdaCase):
    PACKAGE = 'com.ss.iphone.article.News'
    APP_NAME = '今日头条'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
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
            logging.exception('结束今日头条进程失败，继续启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        for _ in range(5):
            button = self.find('不允许', '以后再说', '暂不开启',
                               '我知道了', '取消')
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def start_jrtt(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_main()

    def edge_back(self, wait=3):
        back = self.find('返回', contains=True, max_y=150)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_main(self):
        for _ in range(10):
            nodes = self.nodes()
            home = self.find('首页', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                recommend = self.find('推荐', contains=True, max_y=140)
                if recommend is not None:
                    self.tap_node(recommend)
                    time.sleep(2)
                return
            close = self.find('关闭', '评论关闭', contains=True, nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(2)
            else:
                self.edge_back(wait=2)
        self.fail('多次返回后仍未到达今日头条主界面')

    def open_first_feed_item(self, min_y=140, max_y=700):
        nodes = self.nodes()
        candidates = [n for n in nodes if n.get('visible') == 'true'
                      and n.tag == 'XCUIElementTypeOther'
                      and min_y <= float(n.get('y', 0)) <= max_y
                      and float(n.get('height', 0)) >= 80]
        if candidates:
            self.tap_node(sorted(candidates, key=lambda n: float(n.get('y', 0)))[0])
        else:
            self.device.click(200, 220)
        time.sleep(5)

    def open_video(self):
        self.tap('视频', min_y=740, wait=6)

    def open_video_comments(self):
        comments = self.find('评论', 'comment', contains=True)
        if comments is not None:
            self.tap_node(comments)
        else:
            self.device.click(370, 510)
        time.sleep(4)
