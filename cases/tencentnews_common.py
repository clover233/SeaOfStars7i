"""腾讯新闻动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class TencentNewsCase(WdaCase):
    PACKAGE = 'com.tencent.info'
    APP_NAME = '腾讯新闻'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只在首尾步骤采集，并保证采样窗口不少于 5 秒。"""
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
            logging.exception('结束腾讯新闻进程失败，继续尝试启动')
        time.sleep(1)

    def fail_if_privacy_confirmation_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('同意并继续', nodes=nodes) is not None or
                self.find('用户协议和隐私政策', contains=True,
                          nodes=nodes) is not None):
            self.fail('腾讯新闻尚未确认隐私协议，请先人工确认后再运行')

    def dismiss_optional_prompts(self):
        """关闭非必要授权、引导和开屏广告。"""
        for _ in range(6):
            nodes = self.nodes()
            self.fail_if_privacy_confirmation_required(nodes)
            button = self.find(
                '不允许', '要求App不跟踪', '要求 App 不跟踪',
                '以后再说', '暂不开启', '暂不更新', '我知道了',
                '取消', '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=180, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_tencentnews(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_main()

    def edge_back(self, wait=3):
        back = self.find('返回', contains=True, max_y=150)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_main(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            news_tab = self.find('新闻', min_y=760, nodes=nodes)
            if news_tab is not None:
                self.tap_node(news_tab)
                time.sleep(3)
                headline = self.find('要闻', max_y=150)
                if headline is not None:
                    self.tap_node(headline)
                    time.sleep(3)
                return
            self.edge_back(wait=3)
        self.fail('多次返回后仍未到达腾讯新闻首页')

    def horizontal_browse(self, left, right):
        """左右滑动首页内容区，避免触发系统返回手势。"""
        for _ in range(left):
            self.device.swipe(0.82, 0.5, 0.18, 0.5, 0.3)
            time.sleep(1)
        for _ in range(right):
            self.device.swipe(0.18, 0.5, 0.82, 0.5, 0.3)
            time.sleep(1)
        time.sleep(1)

    def open_first_news(self):
        """点击首页第一条普通新闻，避开视频和底栏入口。"""
        nodes = self.nodes()
        candidates = []
        for node in nodes:
            name = self.node_name(node)
            y = float(node.get('y', 0))
            height = float(node.get('height', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeOther'
                    and name.startswith('QN')
                    and 'NewsCell' in name
                    and 'Video' not in name
                    and 135 <= y <= 720
                    and height >= 35):
                candidates.append(node)
        if candidates:
            candidates.sort(key=lambda node: float(node.get('y', 0)))
            self.tap_node(candidates[0])
        else:
            # 2026-09-16 weditor 实测设备为 402 x 874，首页首条文字
            # 新闻位于顶部频道栏下方；仅在卡片未暴露给 WDA 时使用。
            logging.warning('新闻卡片未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(201, 180)
        time.sleep(6)
        self.wait_article_detail()

    def wait_article_detail(self, timeout=12):
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            back = self.find('返回', contains=True, max_y=150, nodes=nodes)
            article_marker = self.find(
                '写评论', 'comment_button', '分享更多',
                contains=True, min_y=40, nodes=nodes)
            if back is not None and article_marker is not None:
                return
            if time.monotonic() >= deadline:
                self.fail('点击首页新闻后未进入新闻详情页')
            time.sleep(0.5)
