"""美团动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class MeituanCase(WdaCase):
    PACKAGE = 'com.meituan.imeituan'
    APP_NAME = '美团'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只采集指定首尾步骤，并保证每段 trace 不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        """冷启动前清理进程；该动作位于首个 trace 之外。"""
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束美团进程失败，继续尝试启动')
        time.sleep(1)

    def _enable_continuous_ui_mode(self):
        """避免首页动态图文流使 XCTest 长时间等待应用进入 idle。"""
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings({
                'waitForIdleTimeout': 0,
                'animationCoolOffTimeout': 0,
            })
        except Exception:
            logging.exception('设置美团连续页面模式失败，继续使用默认配置')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is None:
            return
        try:
            self.device.appium_settings(previous)
        except Exception:
            logging.exception('恢复 WDA idle 等待设置失败')
        self._previous_idle_settings = None

    def launcher(self):
        try:
            self.dismiss_optional_prompts()
            super().launcher()
        finally:
            self._restore_idle_settings()

    def start_meituan(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        nodes = self.nodes()
        if (self.find('外卖', max_y=360, nodes=nodes) is None or
                self.find('团购', '美食团购', max_y=360,
                          nodes=nodes) is None):
            self.fail('启动后未进入美团主界面')

    def dismiss_optional_prompts(self):
        """关闭会遮挡页面操作、且可能重复出现的系统粘贴授权弹窗。"""
        for _ in range(2):
            button = self.device(name='不允许粘贴')
            if not button.exists:
                return
            button.click()
            time.sleep(1)

    def _point(self, x_ratio, y_ratio):
        size = self.device.window_size()
        return round(size.width * x_ratio), round(size.height * y_ratio)

    def _open_home_entry(self, names, fallback_ratio):
        """优先点击可访问性节点；首页宫格为画布时使用实机比例坐标。"""
        self.dismiss_optional_prompts()
        nodes = self.nodes()
        entry = self.find(*names, max_y=360, nodes=nodes)
        if entry is not None:
            self.tap_node(entry)
        else:
            logging.warning('未找到首页入口 %s，使用 weditor 核对的比例坐标', names)
            self.device.click(*self._point(*fallback_ratio))
        time.sleep(5)
        self.dismiss_optional_prompts()
        self.fail_if_business_page_unavailable()

    def open_takeout(self):
        # 402x874 实机旧版坐标约为 (48, 168)。
        self._open_home_entry(('外卖',), (0.12, 0.192))

    def open_food_group_buy(self):
        # 当前版本首页名称为“团购”；旧版本可能显示“美食团购”。
        self._open_home_entry(('团购', '美食团购'), (0.309, 0.191))

    def fail_if_business_page_unavailable(self):
        nodes = self.nodes()
        errors = (
            '您的网络好像不太给力',
            '网络信号不太好',
            '请稍后再试',
            '访问异常',
            '安全验证',
        )
        for text in errors:
            if self.find(text, contains=True, nodes=nodes) is not None:
                self.fail('业务页面不可用：{}'.format(text))

    def browse(self, up, down):
        """浏览期间持续处理美团可能重复触发的粘贴权限弹窗。"""
        for start, end, count in ((0.75, 0.35, up), (0.35, 0.75, down)):
            for _ in range(count):
                self.dismiss_optional_prompts()
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        self.dismiss_optional_prompts()
        self.fail_if_business_page_unavailable()
        time.sleep(1)

    def return_meituan_home(self):
        """从首页一级业务页执行一次系统侧滑返回。"""
        self.dismiss_optional_prompts()
        self.device.swipe(0.01, 0.50, 0.93, 0.50, 0.35)
        time.sleep(4)
        self.dismiss_optional_prompts()
        nodes = self.nodes()
        has_takeout = self.find('外卖', max_y=360, nodes=nodes) is not None
        has_group_buy = self.find(
            '团购', '美食团购', max_y=360, nodes=nodes) is not None
        if not (has_takeout and has_group_buy):
            self.fail('侧滑返回后未到达美团主界面')
