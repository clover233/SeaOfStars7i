"""滴滴出行动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class DidiCase(WdaCase):
    PACKAGE = 'com.xiaojukeji.didi'
    APP_NAME = '滴滴出行'

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 12)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def _edge_back(self, wait=3):
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(wait)

    def _dismiss_tracking_prompt(self):
        nodes = self.nodes()
        button = self.find('要求App不跟踪', nodes=nodes)
        if button is not None:
            self.tap_node(button)
            time.sleep(3)

    def _is_main_home(self, nodes):
        return (self.find('输入目的地', nodes=nodes) is not None
                and self.find('我的', min_y=740, nodes=nodes) is not None)

    def start_didi(self):
        self.start_app(wait=7)
        self._dismiss_tracking_prompt()
        self.return_home()

    def return_home(self):
        for _ in range(8):
            nodes = self.nodes()
            if self._is_main_home(nodes):
                return
            travel = self.find('出行', max_y=130, nodes=nodes)
            if travel is not None:
                self.tap_node(travel)
                time.sleep(5)
                continue
            home = self.find('首页', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                continue
            back = self.find('返回', nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self._edge_back()
        self.fail('多次返回后仍未到达滴滴首页')

    def open_my(self):
        self.return_home()
        self.tap('我的', min_y=740, wait=5)
        self.wait_for('我的钱包')

    def open_wallet(self):
        self.tap('我的钱包', wait=6)

    def return_wallet_to_my(self):
        # 钱包 WebView 和首次营销弹层均为自绘控件，不读取易为空的页面树。
        self.device.click(200, 632)
        time.sleep(2)
        self.device.click(28, 70)
        time.sleep(5)
        self.wait_for('我的钱包')

    def return_my(self):
        for _ in range(5):
            nodes = self.nodes()
            if (self.find('我的钱包', nodes=nodes) is not None
                    and self.find('我的', min_y=740, nodes=nodes) is not None):
                return
            back = self.find('返回', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                # 2026-09-11 weditor（402×874）：订单等页面左上角返回键为自绘控件。
                self.device.click(20, 84)
            time.sleep(4)
        self.fail('未返回滴滴“我的”页面')

    def open_my_item_and_return(self, name):
        self.tap(name, wait=6)
        self.return_my()

    def open_home_service_and_return(self, name):
        self.return_home()
        nodes = self.nodes()
        node = self.find(name, nodes=nodes)
        if node is None:
            logging.warning('当前滴滴首页无“%s”入口，按用例要求跳过', name)
            return
        self.tap_node(node)
        time.sleep(6)
        self.return_home()

    def open_destination_search(self):
        self.return_home()
        self.tap('输入目的地', wait=4)

    def enter_destination(self, text):
        self.device.send_keys(text)
        time.sleep(4)
        self.wait_for(text, contains=True, timeout=12)

    def browse_destination_results(self, up, down):
        for start, end, count in ((0.55, 0.25, up), (0.25, 0.55, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        time.sleep(1)

    def open_owner(self):
        self.return_home()
        self.tap('车主', max_y=130, wait=6)
        self.wait_for('特惠洗车')

    def return_owner(self):
        for _ in range(6):
            nodes = self.nodes()
            if (self.find('特惠洗车', nodes=nodes) is not None
                    and self.find('车主服务', max_y=150, nodes=nodes) is not None):
                return
            back = self.find('返回', nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self._edge_back()
        self.fail('未返回滴滴车主页面')

    def open_owner_feature(self, requested, current=None):
        self.return_owner()
        current = current or requested
        if current != requested:
            logging.warning('当前滴滴无“%s”入口，使用“%s”替代', requested, current)
        self.tap(current, wait=6)

    def open_owner_more_feature(self, name):
        self.return_owner()
        self.tap('更多', max_y=430, wait=6)
        self.wait_for('全部服务', timeout=12)
        self.tap(name, wait=6)
