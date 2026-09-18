"""知乎动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class ZhihuCase(WdaCase):
    PACKAGE = 'com.zhihu.ios'
    APP_NAME = '知乎'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        self._previous_idle_settings = None
        try:
            settings = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': settings.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': settings.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置知乎 WDA 连续页面模式失败')
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束知乎进程失败，继续启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            settings = getattr(self, '_previous_idle_settings', None)
            if settings is not None:
                try:
                    self.device.appium_settings(settings)
                except Exception:
                    logging.exception('恢复 WDA idle 设置失败')
            self._previous_idle_settings = None

    def dismiss_startup_prompts(self):
        for _ in range(7):
            nodes = self.nodes()
            button = self.find(
                '同意并继续', '同意', '允许', '要求 App 不跟踪',
                '我知道了', '以后再说', '暂不开启', '跳过',
                nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def edge_back(self, wait=3):
        nodes = self.nodes()
        back = self.find(
            'qa.nav_bar.back_button', 'Button:return', '返回',
            contains=True, max_y=150, nodes=nodes)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(4, 437, 350, 437, 0.3)
        time.sleep(wait)

    def is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.find('home_page.recommend', nodes=nodes) is not None
                and self.find('home_page.feed.first', nodes=nodes) is not None)

    def return_zhihu_home(self):
        for _ in range(10):
            nodes = self.nodes()
            if self.is_home(nodes):
                home = self.find('home_page.feed.first', nodes=nodes)
                self.tap_node(home)
                time.sleep(3)
                return
            home = self.find('home_page.feed.first', nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                continue
            close = self.find('PanelHeader:close', nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(2)
                continue
            self.edge_back(wait=3)
        self.fail('多次返回后仍未到达知乎首页')

    def start_zhihu(self):
        self.start_app(wait=0)

    def finish_zhihu_start(self):
        self.dismiss_startup_prompts()
        self.return_zhihu_home()

    def select_home_channel(self, identifier):
        self.tap(identifier, max_y=160, wait=4)

    def open_first_hot_topic(self):
        topics = self.matching_nodes('hot_page.card.title', min_y=200)
        if not topics:
            self.fail('热榜页没有可打开的热榜条目')
        self.tap_node(topics[0])
        time.sleep(6)

    def open_first_answer(self):
        answer = self.find('qa.answer_card_0.container')
        if answer is None:
            self.fail('热榜详情页没有第一条回答')
        self.tap_node(answer)
        time.sleep(6)

    def open_comments(self):
        comments = [node for node in self.nodes()
                    if node.get('visible') == 'true'
                    and self.node_name(node).startswith('评论')
                    and float(node.get('y', 0)) >= 760]
        if not comments:
            self.fail('文章右下角未找到评论按钮')
        comments.sort(key=lambda node: float(node.get('x', 0)))
        self.tap_node(comments[-1])
        time.sleep(5)

    def return_recommend(self):
        self.return_zhihu_home()
        self.select_home_channel('home_page.recommend')

    def search(self, query):
        self.tap('home_page.search', max_y=130, wait=3)
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeTextField',
                                   'XCUIElementTypeTextView')]
        if not fields:
            self.fail('知乎搜索页未找到输入框')
        self.enter_text(query, clear=True)
        self.tap('Search', '搜索', min_y=700, wait=7)

    def open_first_wallpaper_result(self):
        cards = [node for node in self.nodes()
                 if node.get('visible') == 'true'
                 and self.node_name(node) == 'Card:OpenUrl'
                 and 170 <= float(node.get('y', 0)) <= 700
                 and float(node.get('height', 0)) >= 80]
        if not cards:
            self.fail('壁纸搜索结果中没有可打开的条目')
        cards.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(cards[0])
        time.sleep(6)

    def open_first_wallpaper(self):
        images = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeImage'
                  and '的搜索结果' in self.node_name(node)]
        if not images:
            self.fail('壁纸详情页没有可预览的图片')
        images.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(images[0])
        time.sleep(5)

    def browse_wallpapers(self):
        for start, end in ((0.82, 0.18), (0.82, 0.18),
                           (0.18, 0.82), (0.18, 0.82)):
            self.device.swipe(start, 0.5, end, 0.5, 0.3)
            time.sleep(2)

    def open_discover_equivalent(self):
        """新版知乎已将底部“发现”替换为“看山”。"""
        self.tap('home_page.zhida', min_y=760, wait=5)
