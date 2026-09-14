"""懂车帝动态性能用例的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class DongchediCase(WdaCase):
    PACKAGE = 'com.ss.ios.auto'
    APP_NAME = '懂车帝'

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

    def _restart(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(self.PACKAGE)
            time.sleep(0.5)
        except Exception:
            pass
        self.device.app_activate(self.PACKAGE)
        time.sleep(5)

    def _back(self, wait=4):
        back = self.find('返回', '关闭')
        if back is not None:
            self.tap_node(back)
        else:
            # 2026-09-11 weditor（402×874）：车系、图集和图片页返回键仅暴露动态 ID。
            self.device.click(0.06, 0.085)
        time.sleep(wait)

    def start_dongchedi(self):
        self._restart()
        home = self.find('首页', min_y=790)
        if home is not None:
            self.tap_node(home)
            time.sleep(3)
        self.return_recommendation()

    def _channel(self, name, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        channel_names = {'推荐', '直播', '热点', '独家', '政府补贴',
                         '原创', '关注', '赛事', '摩托车', '新车'}
        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeStaticText'
                      and self.node_name(node) == name]
        for candidate in sorted(candidates, key=lambda node: float(node.get('y', 0))):
            y = float(candidate.get('y', 0))
            peers = [node for node in nodes
                     if node.get('visible') == 'true'
                     and node.tag == 'XCUIElementTypeStaticText'
                     and self.node_name(node) in channel_names
                     and abs(float(node.get('y', 0)) - y) <= 4]
            if len(peers) >= 3:
                return candidate
        return None

    def _search_button(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return next((node for node in nodes
                     if node.get('visible') == 'true'
                     and node.tag == 'XCUIElementTypeButton'
                     and self.node_name(node) == '搜索'
                     and float(node.get('x', 0)) > 300
                     and float(node.get('y', 0)) < 750), None)

    def return_recommendation(self):
        for _ in range(6):
            nodes = self.nodes()
            recommendation = self._channel('推荐', nodes)
            if recommendation is not None:
                self.tap_node(recommendation)
                time.sleep(4)
                return
            self.device.swipe(0.2, 0.18, 0.85, 0.18, 0.3)
            time.sleep(1)
        self.fail('频道栏未找到推荐')

    def open_following(self):
        following = self._channel('关注')
        if following is None:
            self.fail('频道栏未找到关注')
        self.tap_node(following)
        time.sleep(4)

    def open_search(self):
        search = self._search_button()
        if search is None:
            self.fail('懂车帝首页未找到搜索按钮')
        self.tap_node(search)
        time.sleep(4)
        self.wait_for_text_field()

    def wait_for_text_field(self, timeout=10):
        deadline = time.monotonic() + timeout
        while True:
            fields = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and node.tag in ('XCUIElementTypeTextField', 'XCUIElementTypeSearchField')
                      and float(node.get('y', 0)) < 130]
            if fields:
                return fields[0]
            if time.monotonic() >= deadline:
                self.fail('未找到懂车帝搜索框')
            time.sleep(0.5)

    def search(self, text):
        field = self.wait_for_text_field()
        self.tap_node(field)
        selector = {'type': field.tag, 'visible': True}
        name = field.get('name')
        if name:
            selector['name'] = name
        element = self.device(**selector)
        element.clear_text()
        element.set_text(text)
        time.sleep(1)
        search = self.find('搜索', max_y=130)
        if search is not None:
            self.tap_node(search)
        else:
            self.tap('Search', wait=1)
        time.sleep(6)
        self.wait_for(text, min_y=140, timeout=15)

    def open_first_search_result(self, text):
        node = self.find(text, min_y=140)
        if node is None:
            self.fail('搜索结果未找到{}'.format(text))
        self.tap_node(node)
        time.sleep(6)

    def open_gallery(self):
        self.tap('图集', max_y=500, wait=3)

    def open_first_picture(self):
        self.device.click(0.5, 0.28)
        time.sleep(5)
        self.wait_for('全部车型')
        self.device.click(0.25, 0.27)
        time.sleep(5)
        if not any(' / ' in self.node_name(node) for node in self.nodes()):
            self.fail('点击第一张图片后未进入图片查看器')

    def browse_pictures(self, left, right):
        for start, end, count in ((0.82, 0.18, left), (0.18, 0.82, right)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.3)
                time.sleep(1)
        time.sleep(1)

    def return_to_gallery(self):
        self._back()
        self.wait_for('全部车型')

    def return_search_landing(self):
        for _ in range(4):
            fields = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and node.tag in ('XCUIElementTypeTextField', 'XCUIElementTypeSearchField')
                      and float(node.get('y', 0)) < 130]
            if fields:
                field = fields[0]
                self.tap_node(field)
                selector = {'type': field.tag, 'visible': True}
                name = field.get('name')
                if name:
                    selector['name'] = name
                self.device(**selector).clear_text()
                time.sleep(4)
                self.wait_for('热榜', timeout=10)
                return
            self._back()
        self.fail('未返回懂车帝搜索界面')

    def open_first_hot_news(self):
        nodes = self.nodes()
        hot = self.find('热榜', nodes=nodes)
        if hot is None:
            self.fail('搜索页未找到热榜')
        hot_y = float(hot.get('y', 0))
        candidates = []
        for node in nodes:
            name = self.node_name(node)
            x = float(node.get('x', 0))
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and x < 280 and hot_y + 25 < y < hot_y + 130
                    and width > 70 and name not in ('更多', '销量排行榜')):
                candidates.append(node)
        if not candidates:
            self.fail('热榜下未找到第一条新闻')
        candidates.sort(key=lambda node: (float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(candidates[0])
        time.sleep(6)

    def return_home(self):
        for _ in range(7):
            nodes = self.nodes()
            home = self.find('首页', min_y=790, nodes=nodes)
            search = self._search_button(nodes)
            if home is not None and search is not None:
                self.tap_node(home)
                time.sleep(3)
                return
            self._back()
        self.fail('多次返回后仍未到达懂车帝主界面')
