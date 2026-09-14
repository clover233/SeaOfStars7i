"""米家动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class MiHomeCase(WdaCase):
    PACKAGE = 'com.xiaomi.mihome'
    APP_NAME = '米家'

    def _dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            if self.find('人车家生态数据授权', contains=True, nodes=nodes):
                self.device.click(115, 791)
                time.sleep(3)
                continue
            button = self.find('允许', '取消', '以后再说', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(3)

    def start_mihome(self):
        self.start_app(wait=7)
        self._dismiss_optional_prompts()
        self.return_home()

    def return_home(self):
        for _ in range(6):
            nodes = self.nodes()
            home = self.find('米家', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                return
            back = self.find('返回', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.click(22, 78)
            time.sleep(3)
        self.fail('未返回米家主界面')

    def open_tab(self, name):
        self.tap(name, min_y=740, wait=4)

    def open_go_home(self):
        for _ in range(5):
            nodes = self.nodes()
            target = self.find('回家', nodes=nodes)
            if target is not None:
                self.tap_node(target)
                time.sleep(4)
                return
            target = self.find('手机回家模式', nodes=nodes)
            if target is not None:
                logging.warning('当前米家无独立“回家”入口，使用“手机回家模式”替代')
                self.tap_node(target)
                time.sleep(4)
                return
            self.device.swipe(0.5, 0.72, 0.5, 0.35, 0.3)
            time.sleep(2)
        self.fail('智能页未找到“回家”或“手机回家模式”')

    def open_add_device(self):
        self.return_home()
        self.tap('添加', max_y=130, wait=2)
        self.tap('弹出式窗口、添加设备', '添加设备', wait=6)
        if self.find('扫描附近设备', contains=True) is None:
            self.fail('点击添加设备后未进入添加设备页')
