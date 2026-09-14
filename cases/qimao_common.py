"""七猫免费小说动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class QimaoCase(WdaCase):
    PACKAGE = 'com.yueyou.cyreader'
    APP_NAME = '七猫免费小说'

    def prepare_iteration(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        self.device.app_terminate(self.PACKAGE)
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

    def dismiss_optional_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            prompt = self.find(
                '同意并继续', '同意', '不允许', '以后再说', '暂不',
                '我知道了', 'ic icon close big', nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(1)

    def edge_back(self):
        self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(2)

    def return_book_city(self):
        for _ in range(7):
            nodes = self.nodes()
            book_city = self.find('书城', min_y=760, nodes=nodes)
            if book_city is not None:
                self.tap_node(book_city)
                time.sleep(3)
                self.dismiss_optional_prompts()
                return
            back = self.find(
                'app bar btn back default', '返回', max_y=140, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(2)
            else:
                self.edge_back()
        self.fail('多次返回后仍未到达七猫主界面')

    def start_qimao(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_book_city()

    def turn_pages(self, left, right):
        # 2026-09-14 weditor（402×874）：阅读正文由画布绘制，无可访问节点。
        for start, end, count in ((0.82, 0.18, left), (0.18, 0.82, right)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.3)
                time.sleep(1)
        time.sleep(1)

    def open_search(self):
        nodes = self.nodes()
        search = self.find(
            'book_icon_search', 'app bar icon withtext search d',
            max_y=160, nodes=nodes)
        if search is not None:
            self.tap_node(search)
        else:
            logging.warning('七猫搜索图标未暴露，使用 weditor 核对坐标')
            self.device.click(33, 89)
        time.sleep(3)
        self.wait_for('搜索', max_y=130, timeout=8)

    def search_book(self, keyword):
        self.enter_text(keyword, clear=True)
        self.tap('搜索', max_y=130, wait=5)
        self.wait_for(keyword, contains=True, min_y=140, timeout=12)
