"""云闪付动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class CloudFlashPayCase(WdaCase):
    PACKAGE = 'com.unionpay.chsp'
    APP_NAME = '云闪付'

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

    def start_cloudflashpay(self):
        self.start_app(wait=6)
        self.return_home()
        floating_close = self.find('frog_flow_dogCLose')
        if floating_close is not None:
            self.tap_node(floating_close)
            time.sleep(1)
        self.wait_for('收付款', contains=True, max_y=250)

    def return_home(self):
        for _ in range(8):
            nodes = self.nodes()
            back_home = self.find('回到首页', nodes=nodes)
            if back_home is not None:
                self.tap_node(back_home)
                time.sleep(3)
                continue
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                if self.find('收付款', contains=True, max_y=250) is not None:
                    return
                continue
            back = self.find('返回', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达云闪付首页')

    def browse_cycles(self, repeats, up_count=1, down_count=1):
        """按用例要求每轮先上滑再下滑，不改变页面落点。"""
        for _ in range(repeats):
            for _ in range(up_count):
                self.device.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
                time.sleep(1)
            for _ in range(down_count):
                self.device.swipe(0.5, 0.35, 0.5, 0.75, 0.3)
                time.sleep(1)
        time.sleep(1)

    def open_pay_and_return(self):
        self.return_home()
        self.tap('收付款', contains=True, max_y=250, wait=3)
        self.wait_for('返回', max_y=130)
        self.return_home()

    def open_scanner(self):
        self.tap('扫一扫', contains=True, max_y=250, wait=3)
        self.wait_for('扫二维码 / 条码')

    def return_home_and_open_scanner(self):
        self.return_home()
        self.open_scanner()

    def open_discount(self):
        self.return_home()
        self.tap('优惠', min_y=760, wait=5)
        self.wait_for('热门推荐')

    def open_benefit_life(self):
        nodes = self.nodes()
        target = self.find('惠生活', nodes=nodes)
        if target is None:
            logging.warning('当前云闪付已无“惠生活”，使用优惠页“生活”分类替代')
            target = self.find('生活', nodes=nodes)
        if target is None:
            self.fail('优惠页未找到“惠生活”或“生活”')
        self.tap_node(target)
        time.sleep(4)

    def open_food(self):
        self.tap('美食', wait=4)
