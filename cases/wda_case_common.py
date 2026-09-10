"""iOS 动态性能用例的 WDA 公共能力。"""

import logging
import os
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager

from aw import SeaOfStarsAW
from cases.CaseBase import Case


class WdaCase(Case):
    PACKAGE = None
    APP_NAME = '应用'
    all_app_package_list = []
    TEST_TIME = 1
    STEP_INTERVAL = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__
        self.current_step = '准备环境'
        self._has_step = False
        self._trace_active = False

    @property
    def device(self):
        return SeaOfStarsAW.ut_device

    @contextmanager
    def capture_trace(self, iteration, step_number):
        """只包围首尾单步；每轮固定生成两份短 trace。"""
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        if step_number == 1:
            self._has_step = False
        try:
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'round_{}_step_{}'.format(iteration + 1, step_number),
                self.screenshot_dir_path,
            )
            self._trace_active = True
            yield
        finally:
            self._trace_active = False
            SeaOfStarsAW.stop_trace()

    @SeaOfStarsAW.function_log
    def set_up(self):
        if self.PACKAGE is None or self.device.app_state(self.PACKAGE)['value'] == 0:
            raise RuntimeError('设备未安装{}'.format(self.APP_NAME))
        return True

    def step(self, number, text):
        if self._has_step:
            time.sleep(self.STEP_INTERVAL)
        self._has_step = True
        self.current_step = '{}、{}'.format(number, text)
        logging.info(self.current_step)
        if self._trace_active and SeaOfStarsAW.trace_thread is not None:
            SeaOfStarsAW.trace_thread.add_log(self.APP_NAME, self.current_step)

    def fail(self, message):
        path = os.path.join(
            self.screenshot_dir_path,
            'step_{}_failed.png'.format(self.current_step.split('、')[0]),
        )
        try:
            self.device.screenshot(path)
        except Exception:
            logging.exception('失败截图保存失败')
        raise AssertionError('{}：{}'.format(self.current_step, message))

    def nodes(self):
        # 百度 WebView 页面切换时偶尔返回一次空 source，短暂重试避免误判。
        for _ in range(3):
            source = self.device.source()
            if source and source.strip():
                return list(ET.fromstring(source).iter())
            time.sleep(0.5)
        self.fail('WDA 未返回页面层级')

    @staticmethod
    def node_name(node):
        return node.get('name') or node.get('label') or node.get('value') or ''

    def matching_nodes(self, *names, min_y=None, max_y=None, contains=False, nodes=None):
        result = []
        for node in self.nodes() if nodes is None else nodes:
            if node.get('visible') != 'true' or node.get('enabled') == 'false':
                continue
            name = self.node_name(node)
            if not name:
                continue
            y = float(node.get('y', 0))
            if min_y is not None and y < min_y:
                continue
            if max_y is not None and y > max_y:
                continue
            matched = any(candidate == name for candidate in names)
            if contains:
                matched = matched or any(candidate in name for candidate in names)
            if matched:
                result.append(node)
        return sorted(result, key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))

    def find(self, *names, **kwargs):
        matches = self.matching_nodes(*names, **kwargs)
        return matches[0] if matches else None

    def tap_node(self, node):
        x, y, width, height = (float(node.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        if width <= 0 or height <= 0:
            self.fail('控件没有可点击区域：{}'.format(self.node_name(node)))
        # facebook-wda 会把 float 当百分比，绝对坐标必须转成 int。
        self.device.click(round(x + width / 2), round(y + height / 2))

    def tap(self, *names, fallback=None, wait=2, timeout=6, min_y=None,
            max_y=None, contains=False, choose='first'):
        deadline = time.monotonic() + timeout
        while True:
            matches = self.matching_nodes(
                *names, min_y=min_y, max_y=max_y, contains=contains)
            if matches:
                self.tap_node(matches[-1] if choose == 'last' else matches[0])
                break
            if time.monotonic() >= deadline:
                if fallback is None:
                    self.fail('未找到控件：{}'.format(' / '.join(names)))
                logging.warning('控件 %s 不可访问，使用 weditor 核对坐标 %s', names, fallback)
                self.device.click(*fallback)
                break
            time.sleep(0.5)
        time.sleep(max(self.STEP_INTERVAL, wait))

    def start_app(self, wait=4):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        self.device.app_activate(self.PACKAGE)
        time.sleep(wait)

    def enter_text(self, text, clear=False):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeTextField', 'XCUIElementTypeTextView')]
        if fields:
            node = fields[-1]
            selector = {'type': node.tag, 'visible': True}
            name = node.get('name')
            if name:
                selector['name'] = name
            element = self.device(**selector)
            if clear:
                element.clear_text()
            element.set_text(text)
        else:
            # 百度和百度地图的聚焦输入框由 WebView/画布绘制，不在 WDA 树中。
            self.device.send_keys(text)
        time.sleep(1)

    def browse(self, up, down):
        for start, end, count in ((0.75, 0.35, up), (0.35, 0.75, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        time.sleep(1)

    def launcher(self):
        for _ in range(2):
            self.device.swipe(0.5, 0.995, 0.5, 0.15, 0.1)
            time.sleep(2)
            if self.device.app_current().get('bundleId') == 'com.apple.springboard':
                return
        self.fail('滑动后未回到 Home 页')
