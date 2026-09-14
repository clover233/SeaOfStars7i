import logging
import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_mms_0010(WdaCase):
    """Excel 7.0.2：进入通知类信息列表并浏览两条信息。"""

    PACKAGE = 'com.apple.MobileSMS'
    APP_NAME = '信息'

    def ensure_message_list(self):
        for _ in range(3):
            if self.find('filteringButton') is not None:
                return
            back = self.find('BackButton', '返回')
            if back is None:
                self.fail('信息应用未处于可返回的会话或列表页面')
            self.tap_node(back)
            time.sleep(2)
        self.fail('未能返回信息列表')

    def open_notification_list(self):
        self.tap('filteringButton', wait=1)
        nodes = self.nodes()
        entry = self.find('通知信息', nodes=nodes)
        if entry is None:
            entry = self.find('未知发件人', nodes=nodes)
            if entry is not None:
                logging.info('当前 iOS 版本以“未知发件人”显示通知信息入口')
        if entry is None:
            self.fail('未找到“通知信息/未知发件人”入口')
        self.tap_node(entry)
        time.sleep(3)

    def first_message_cell(self):
        seen = set()
        for node in self.nodes():
            if node.tag != 'XCUIElementTypeCell' or node.get('visible') != 'true':
                continue
            bounds = tuple(node.get(key) for key in ('x', 'y', 'width', 'height'))
            if bounds in seen:
                continue
            seen.add(bounds)
            y = float(node.get('y', 0))
            height = float(node.get('height', 0))
            if y >= 110 and height >= 50:
                return node
        self.fail('通知信息列表中没有可打开的信息；请至少预置一条通知类短信')

    def back_to_message_list(self):
        self.tap('BackButton', '返回', wait=3)

    def back_to_main(self):
        self.tap('filteringButton', wait=1)
        self.tap('信息', wait=3)

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动信息')
                self.start_app(wait=5)
            self.ensure_message_list()

            self.step(2, '点击通知信息，进入通知信息页面')
            self.open_notification_list()

            self.step(3, '浏览通知信息，上滑5次，下滑5次')
            self.browse(5, 5)

            self.step(4, '打开一条通知信息进行查看，重复操作2次')
            for _ in range(2):
                self.tap_node(self.first_message_cell())
                time.sleep(3)
                self.back_to_message_list()

            self.step(5, '返回信息主界面')
            self.back_to_main()

            with self.capture_trace(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
