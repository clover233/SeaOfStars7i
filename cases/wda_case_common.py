"""iOS 动态性能用例的 WDA 公共能力。"""

import base64
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
    CHECK_STEP_FOREGROUND = False
    SOURCE_TIMEOUT = None

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__
        self.current_step = '准备环境'
        self._has_step = False
        self._trace_active = False
        self._trace_iteration = 0
        self._trace_step_number = None

    @property
    def device(self):
        return SeaOfStarsAW.ut_device

    @contextmanager
    def capture_trace(self, iteration, step_number):
        """记录当前轮次，并在显式上下文结束时收尾当前步骤。"""
        self._trace_iteration = iteration
        if step_number == 1:
            self._has_step = False
        try:
            yield
        finally:
            if self._trace_active and self._trace_step_number == step_number:
                SeaOfStarsAW.stop_trace()
                self._trace_active = False
                self._trace_step_number = None

    def _start_step_trace(self, step_number):
        """为每个用例步骤单独生成一份 trace 日志。"""
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        if self._trace_active:
            SeaOfStarsAW.stop_trace()
        SeaOfStarsAW.start_trace(
            self.trace_dir_path,
            self.__class__.__name__,
            'step_{}'.format(step_number),
            self.screenshot_dir_path,
        )
        self._trace_active = True
        self._trace_step_number = step_number

    @SeaOfStarsAW.function_log
    def set_up(self):
        if self.PACKAGE is None or self.device.app_state(self.PACKAGE)['value'] == 0:
            raise RuntimeError('设备未安装{}'.format(self.APP_NAME))
        return True

    def step(self, number, text):
        self.current_step = '{}、{}'.format(number, text)
        self.check_step_foreground(number)
        if self._has_step:
            time.sleep(self.STEP_INTERVAL)
        self._has_step = True
        self._start_step_trace(number)
        logging.info(self.current_step)
        SeaOfStarsAW.trace_thread.add_log(self.APP_NAME, self.current_step)

    def check_step_foreground(self, number):
        """视频用例在步骤边界恢复后台应用；进程退出时终止本轮。"""
        if not self.CHECK_STEP_FOREGROUND or number == 1:
            return
        state = self.device._session_http.post(
            '/wda/apps/state', {'bundleId': self.PACKAGE}, timeout=15)['value']
        if state == 4:  # XCUIApplicationStateRunningForeground
            return
        if state not in (2, 3):
            raise RuntimeError('{}进程已退出，需从首步重新运行用例'.format(self.APP_NAME))
        logging.warning('%s已进入后台（state=%s），重新激活后继续', self.APP_NAME, state)
        self.device._session_http.post(
            '/wda/apps/activate', {'bundleId': self.PACKAGE}, timeout=15)
        time.sleep(2)
        state = self.device._session_http.post(
            '/wda/apps/state', {'bundleId': self.PACKAGE}, timeout=15)['value']
        if state != 4:
            raise RuntimeError('{}未恢复到前台，请检查锁屏和系统弹窗'.format(self.APP_NAME))

    def fail(self, message):
        path = os.path.join(
            self.screenshot_dir_path,
            'step_{}_failed.png'.format(self.current_step.split('、')[0]),
        )
        try:
            if self.SOURCE_TIMEOUT is None:
                self.device.screenshot(path)
            else:
                data = self.device.http.get('screenshot', timeout=8).value
                with open(path, 'wb') as output:
                    output.write(base64.b64decode(data))
        except Exception:
            logging.exception('失败截图保存失败')
        raise AssertionError('{}：{}'.format(self.current_step, message))

    def nodes(self):
        # 百度 WebView 页面切换时偶尔返回一次空 source，短暂重试避免误判。
        for _ in range(3):
            if self.SOURCE_TIMEOUT is None:
                source = self.device.source()
            else:
                source = self.device.http.get(
                    'source?format=xml', timeout=self.SOURCE_TIMEOUT).value
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

    def tap_viewport(self, x, y):
        """用 WDA W3C 动作点击整数屏幕坐标，避免坐标 tap 隐含的 frame 查询。"""
        self.device._session_http.post('/actions', {'actions': [{
            'type': 'pointer', 'id': 'screen_touch',
            'parameters': {'pointerType': 'touch'},
            'actions': [
                {'type': 'pointerMove', 'duration': 0, 'origin': 'viewport',
                 'x': round(x), 'y': round(y)},
                {'type': 'pointerDown', 'button': 0},
                {'type': 'pause', 'duration': 80},
                {'type': 'pointerUp', 'button': 0},
            ],
        }]}, timeout=30)

    def swipe_viewport(self, x1, y1, x2, y2, duration=0.3):
        """通过 WDA W3C viewport 坐标滑动，不查询应用 frame。"""
        self.device._session_http.post('/actions', {'actions': [{
            'type': 'pointer', 'id': 'screen_swipe',
            'parameters': {'pointerType': 'touch'},
            'actions': [
                {'type': 'pointerMove', 'duration': 0, 'origin': 'viewport',
                 'x': round(x1), 'y': round(y1)},
                {'type': 'pointerDown', 'button': 0},
                {'type': 'pointerMove', 'duration': round(duration * 1000),
                 'origin': 'viewport', 'x': round(x2), 'y': round(y2)},
                {'type': 'pointerUp', 'button': 0},
            ],
        }]}, timeout=30)

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
        # 蛋仔派对等横屏全屏游戏会拦截底部手势；仍先执行两次真实滑动，
        # 失败时再使用 WDA 的 Home-screen 接口完成同一退出结果。
        self.device.home()
        time.sleep(2)
        if self.device.app_current().get('bundleId') == 'com.apple.springboard':
            return
        self.fail('滑动后未回到 Home 页')
