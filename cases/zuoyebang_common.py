"""作业帮 iOS 动态性能用例公共能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class ZuoyebangCase(WdaCase):
    PACKAGE = 'com.baidu.homework'
    APP_NAME = '作业帮'

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
            logging.exception('设置作业帮连续页面模式失败')

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
            logging.exception('结束作业帮进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        for _ in range(5):
            nodes = self.nodes()
            # 相机是该用例的必要预置权限，不在运行中临时修改系统权限。
            names = [self.node_name(node) for node in nodes]
            if any('相机' in name and any(text in name for text in (
                    '权限', '允许', '访问', '设置中开启')) for name in names):
                self.fail('请先在系统设置中授予作业帮相机权限，再运行用例')
            button = self.find(
                '要求App不跟踪', '要求 App 不跟踪', '不允许', '以后再说',
                '下次再说', '暂不开启', '暂不更新', '我知道了', '取消',
                '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        has_home = self.find('首页', min_y=720, nodes=nodes) is not None
        has_entry = any(self.find(name, contains=True, nodes=nodes) is not None
                        for name in ('搜索答疑', '作业批改', 'aihome navi search'))
        return has_home and has_entry

    def return_home(self):
        for _ in range(7):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_home(nodes):
                return
            home = self.find('首页', min_y=720, nodes=nodes)
            if home is not None:
                self.tap_node(home)
            else:
                back = self.find('返回', '关闭', 'camera close new',
                                 max_y=180, nodes=nodes)
                if back is not None:
                    self.tap_node(back)
                else:
                    self.device.swipe(0.01, 0.5, 0.90, 0.5, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达作业帮主界面')

    def start_zuoyebang(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()

    def open_search_answer(self):
        self.tap('搜索答疑', fallback=(92, 252), contains=True, wait=5)

    def take_photo(self):
        self.dismiss_optional_prompts()
        self.tap('拍照', 'camera shutter', fallback=(201, 798),
                 contains=True, min_y=650, wait=5)

    def close_camera_to_home(self):
        for _ in range(2):
            nodes = self.nodes()
            close = self.find('camera close new', '关闭', '返回',
                              max_y=220, nodes=nodes)
            if close is not None:
                self.tap_node(close)
            else:
                self.device.click(30, 70)
            time.sleep(2)
        self.return_home()

    def open_homework_correction(self):
        self.tap('作业批改', fallback=(201, 252), contains=True, wait=5)

    def close_camera_once(self):
        nodes = self.nodes()
        close = self.find('camera close new', '关闭', '返回',
                          max_y=220, nodes=nodes)
        if close is not None:
            self.tap_node(close)
        else:
            self.device.click(30, 70)
        time.sleep(3)
        self.return_home()

    def open_practice(self):
        self.tap('练习', '同步学练', '同步练习', fallback=(120, 820),
                 contains=True, min_y=650, wait=5)

    def open_vip(self):
        self.tap('VIP', '会员', fallback=(282, 820),
                 contains=True, min_y=650, wait=5)

    def open_learning_goods(self):
        self.tap('学习好物', fallback=(356, 820), contains=True,
                 min_y=600, wait=6)

    def focus_home_search(self):
        self.tap('aihome navi search', '搜索', fallback=(201, 91),
                 contains=True, max_y=180, wait=2)

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        self.tap('Search', '搜索', fallback=(355, 825),
                 min_y=720, choose='last', wait=8)

    def open_more_results(self):
        self.tap('查看更多', fallback=(201, 730), contains=True,
                 min_y=180, wait=5)

    def like_result(self):
        self.tap('赞', '点赞', '值得鼓励', fallback=(340, 640),
                 contains=True, min_y=180, wait=3)
