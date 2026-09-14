"""华为运动健康动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class HuaweiHealthCase(WdaCase):
    PACKAGE = 'com.huawei.iossporthealth'
    APP_NAME = '华为运动健康'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾维测打点至少覆盖 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                remaining = 5 - (time.monotonic() - started_at)
                if remaining > 0:
                    time.sleep(remaining)

    def prepare_iteration(self):
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束华为运动健康进程失败，继续尝试启动')
        time.sleep(1)

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 10)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def _dismiss_optional_guides(self):
        """关闭运营横幅和设备页引导，不自动处理系统权限。"""
        for _ in range(5):
            nodes = self.nodes()
            button = self.find(
                '忽略', '知道了', 'ico close2', 'ic small close', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def _fail_if_system_permission_prompt(self, permission):
        current = self.device.app_current().get('bundleId')
        markers = ('想要使用您的位置', '想访问您的相机', '使用你的位置',
                   '访问相机', 'Camera', 'Location')
        source_names = ' '.join(self.node_name(node) for node in self.nodes())
        if current == 'com.apple.springboard' or any(
                marker in source_names for marker in markers):
            self.fail('请先在系统设置中允许华为运动健康使用{}权限'.format(permission))

    def normalize_home_after_launch(self):
        self._dismiss_optional_guides()
        self.return_health_main()

    def return_health_main(self):
        """从功能页回到“健康/今日”主页面。"""
        for _ in range(10):
            nodes = self.nodes()
            health = self.find(
                'AT_home_btn_health', '今日', '健康', min_y=740, nodes=nodes)
            if health is not None:
                self.tap_node(health)
                time.sleep(3)
                self._dismiss_optional_guides()
                return
            back = self.find('返回', '返回。按钮', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达华为运动健康主界面')

    def open_outdoor_running(self):
        self.tap('AT_home_btn_sports', '锻炼', min_y=740, wait=4)
        self.tap('户外跑步', max_y=180, wait=3)
        self.tap('开始运动', 'GO', min_y=600, wait=5)
        self._fail_if_system_permission_prompt('定位')
        self.wait_for('暂停', min_y=650, timeout=12)

    def finish_short_workout(self, seconds=15):
        time.sleep(seconds)
        self.tap('暂停', min_y=650, wait=2)
        end = self.wait_for('结束运动', min_y=650, timeout=8)
        x, y, width, height = (float(end.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        self.device.tap_hold(
            round(x + width / 2), round(y + height / 2), duration=2.5)
        time.sleep(3)

        # 15 秒通常达不到保存阈值，确认结束但不会产生运动记录。
        buttons = [node for node in self.matching_nodes('结束运动', min_y=350)
                   if node.tag == 'XCUIElementTypeButton']
        if buttons:
            self.tap_node(buttons[-1])
            time.sleep(4)
        self.wait_for('开始运动', '户外跑步', timeout=12)

    def open_today(self):
        # 工作簿写“今日”，当前 16.1.71 版本底部标签显示为“健康”。
        self.tap('AT_home_btn_health', '今日', '健康', min_y=740, wait=4)

    def open_clover_details(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true' and name == '活力三环'
                    and x >= 290 and y <= 260 and width <= 100
                    and height <= 100):
                candidates.append(node)
        if not candidates:
            self.fail('健康页未找到右上角三叶草/活力三环入口')
        self.tap_node(candidates[0])
        time.sleep(4)
        self.wait_for('健康生活', '开启健康生活', contains=True, timeout=10)

    def open_devices(self):
        self.tap('AT_home_btn_device', '设备', min_y=740, wait=5)
        self._dismiss_optional_guides()
        self.wait_for('设备', max_y=130, timeout=10)

    def open_more_functions(self):
        self.tap('更多选项按钮', '更多选项', max_y=130, wait=2)
        self.wait_for('扫一扫', max_y=260, timeout=8)

    def scan_and_return(self):
        self.tap('扫一扫', max_y=260, wait=4)
        self._fail_if_system_permission_prompt('相机')
        self.wait_for('图库选择', '返回', max_y=130, timeout=10)
        self.tap('返回', '返回。按钮', max_y=130, wait=4)
        self.wait_for('设备', max_y=130, timeout=10)

