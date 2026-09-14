"""华为商城动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class HuaweiMallCase(WdaCase):
    PACKAGE = 'com.vmall.ios'
    APP_NAME = '华为商城'

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
            logging.exception('结束华为商城进程失败，继续尝试启动')
        time.sleep(1)

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

    def _contains(self, text, nodes=None):
        return self.find(text, contains=True, nodes=nodes)

    def normalize_home_after_launch(self):
        self.return_home()

    def return_home(self):
        """退出搜索、详情、评价或客服页并回到商城首页。"""
        for _ in range(12):
            nodes = self.nodes()
            # 商品详情底部有独立的“首页”按钮，优先使用。
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(5)
                nodes = self.nodes()
                if self._contains('搜索框', nodes=nodes) is not None:
                    return

            result_back = self.find('searchresult-back', nodes=nodes)
            if result_back is not None:
                self.tap_node(result_back)
            else:
                # 商城 Web 页面统一使用左上角圆形返回按钮，但未暴露名称。
                self.device.click(42, 82)
            time.sleep(4)

            nodes = self.nodes()
            if self._contains('搜索框', nodes=nodes) is not None:
                bottom_home = self.find('首页', min_y=760, nodes=nodes)
                if bottom_home is not None:
                    self.tap_node(bottom_home)
                    time.sleep(4)
                return
        self.fail('多次返回后仍未到达华为商城首页')

    def _visible_carousel_card(self):
        cards = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true' and name.startswith('Picture-')
                    and 'Whole' not in name and 0 <= x <= 40
                    and 100 <= y <= 180 and 300 <= width <= 380
                    and height >= 250):
                cards.append(node)
        return cards[0] if cards else None

    def advance_carousel(self):
        self.device.swipe(350, 300, 50, 300, 0.3)
        time.sleep(3)

    def open_current_carousel(self):
        card = self._visible_carousel_card()
        if card is None:
            logging.warning('轮播图未暴露可访问节点，使用 weditor 核对坐标')
            self.device.click(200, 300)
        else:
            self.tap_node(card)
        time.sleep(6)
        self.wait_for('prd-detail', timeout=15)

    def open_search(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true' and '搜索框' in name
                    and y <= 110 and x >= 10 and width >= 220
                    and height <= 70):
                candidates.append(node)
        if not candidates:
            self.fail('商城首页未找到搜索框')
        self.tap_node(sorted(candidates, key=lambda node: float(
            node.get('width', 0)))[0])
        time.sleep(4)
        self.wait_for('vui_searchbar_input', timeout=10)

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        nodes = self.nodes()
        buttons = [node for node in self.matching_nodes('搜索', nodes=nodes)
                   if node.tag == 'XCUIElementTypeButton']
        if not buttons:
            self.fail('搜索页未找到“搜索”按钮')
        self.tap_node(buttons[0])
        time.sleep(6)
        self.wait_for('0-searchProduct', timeout=15)

    def open_first_search_product(self):
        self.tap('0-searchProduct', wait=6)
        self.wait_for('prd-detail', timeout=15)

    def open_category(self):
        self.tap('分类', min_y=760, wait=5)
        self.wait_for('分类', max_y=130, timeout=12)

    def _first_category_product(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true' and '元' in name
                    and x >= 90 and y >= 190 and 250 <= width <= 300
                    and 65 <= height <= 100):
                candidates.append(node)
        if not candidates:
            self.fail('分类页未找到可见商品')
        return sorted(candidates, key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))[0]

    def open_first_category_product(self):
        self.tap_node(self._first_category_product())
        time.sleep(6)
        self.wait_for('prd-detail', timeout=15)

    def return_to_category(self):
        self.device.click(42, 82)
        time.sleep(5)
        self.wait_for('分类', max_y=130, timeout=12)

    def swipe_up_once(self):
        self.device.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
        time.sleep(3)

    def show_review_section(self):
        self.tap('评价', max_y=180, wait=4)
        self.wait_for('查看全部评价', contains=True, timeout=12)

    def open_all_reviews(self):
        card = self.wait_for('查看全部评价', contains=True, timeout=12)
        y = float(card.get('y', 0))
        self.device.click(330, round(y + 40))
        time.sleep(5)
        self.wait_for('商品评价', max_y=130, timeout=12)

    def return_to_product(self):
        self.device.click(42, 82)
        time.sleep(5)
        self.wait_for('prd-detail', timeout=12)

    def open_customer_service(self):
        self.tap('客服', min_y=760, wait=6)
        self.wait_for('华为商城客户服务', timeout=15)

    def return_from_customer_service(self):
        # 首次进入可能显示“开始聊天”隐私说明，本用例只进入后返回。
        self.device.click(42, 82)
        time.sleep(5)
        self.wait_for('prd-detail', timeout=12)
