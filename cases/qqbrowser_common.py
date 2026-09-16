"""QQ 浏览器动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class QqBrowserCase(WdaCase):
    PACKAGE = 'com.tencent.mttlite'
    APP_NAME = 'QQ浏览器'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾维测打点至少覆盖 xctrace 的 5 秒采样窗口。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束QQ浏览器进程失败，继续尝试启动')
        time.sleep(1)

    def dismiss_optional_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            if self.find('这里发现更多网页工具～', nodes=nodes) is not None:
                # 2026-09-15 weditor（402×874）：该引导的关闭图标没有
                # accessibility name，位于浮层右上角。
                self.device.click(362, 580)
                time.sleep(2)
                continue
            button = self.find(
                '同意并继续', '不允许', '以后再说', '暂不', '我知道了',
                nodes=nodes,
            )
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def start_qqbrowser(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_browser_home()

    def return_browser_home(self):
        for _ in range(6):
            nodes = self.nodes()
            if (self.find('home_page_search_box', nodes=nodes) is not None
                    or self.find('搜索或输入网址', nodes=nodes) is not None):
                return
            start_page = self.find('起始页', min_y=740, nodes=nodes)
            if start_page is not None:
                self.tap_node(start_page)
                time.sleep(4)
                self.dismiss_optional_prompts()
                continue
            back = self.find('后退', min_y=740, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
                continue
            self.device.swipe(4, 437, 354, 437, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达QQ浏览器主界面')

    def open_search(self):
        nodes = self.nodes()
        search = self.find(
            'home_page_search_box', '搜索或输入网址', nodes=nodes)
        if search is None:
            self.fail('QQ浏览器首页未找到搜索框')
        self.tap_node(search)
        time.sleep(3)
        if not any(node.tag in ('XCUIElementTypeTextField',
                                'XCUIElementTypeTextView')
                   for node in self.nodes()):
            self.fail('点击搜索框后未进入输入状态')

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        self.tap('搜索按钮', '搜索', max_y=130, wait=7)
        self.dismiss_optional_prompts()

    def browse_page(self, up, down):
        for _ in range(up):
            self.device.swipe_up()
            time.sleep(1)
        for _ in range(down):
            self.device.swipe_down()
            time.sleep(1)
        time.sleep(1)

    def open_chsi_result(self):
        nodes = self.nodes()
        matches = [
            node for node in nodes
            if node.get('visible') == 'true'
            and node.tag == 'XCUIElementTypeLink'
            and '中国高等教育学生信息网' in self.node_name(node)
            and 150 <= float(node.get('y', 0)) <= 600
        ]
        if not matches:
            self.fail('搜索结果中未找到学信网官网，请检查网络和搜索结果')
        matches.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(matches[0])
        time.sleep(7)
        self.dismiss_optional_prompts()
        if self.find('学信网', contains=True, max_y=250) is None:
            self.fail('点击首条搜索结果后未进入学信网官网')

    def open_first_chsi_content(self):
        nodes = self.nodes()
        preferred = self.find('从《教育发展', contains=True, nodes=nodes)
        if preferred is not None:
            self.tap_node(preferred)
        else:
            candidates = [
                node for node in nodes
                if node.get('visible') == 'true'
                and node.tag == 'XCUIElementTypeLink'
                and 280 <= float(node.get('y', 0)) <= 700
                and float(node.get('width', 0)) >= 180
                and self.node_name(node) not in ('学信网', '更多')
                and '更多专题' not in self.node_name(node)
            ]
            if not candidates:
                self.fail('学信网首页未找到可打开的第一条内容')
            candidates.sort(key=lambda node: float(node.get('y', 0)))
            self.tap_node(candidates[0])
        time.sleep(7)
        if self.find('后退', min_y=740) is None:
            self.fail('点击学信网第一条内容后未进入详情页')
