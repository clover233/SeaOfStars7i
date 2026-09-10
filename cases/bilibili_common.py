"""哔哩哔哩动态性能用例的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class BilibiliCase(WdaCase):
    PACKAGE = 'tv.danmaku.bilianime'
    APP_NAME = '哔哩哔哩'

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 8)
        contains = kwargs.pop('contains', False)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, contains=contains, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def start_bilibili(self):
        self.start_app(wait=4)
        self.wait_for('搜索栏')

    def open_channel(self, name):
        self.tap(name, min_y=100, max_y=150, wait=3)

    def _tap_first_matching(self, predicate, description, timeout=8):
        deadline = time.monotonic() + timeout
        while True:
            candidates = []
            for node in self.nodes():
                if node.get('visible') != 'true' or node.get('enabled') == 'false':
                    continue
                if predicate(node):
                    candidates.append(node)
            if candidates:
                candidates.sort(key=lambda node: (
                    float(node.get('y', 0)), float(node.get('x', 0))))
                self.tap_node(candidates[0])
                time.sleep(5)
                return
            if time.monotonic() >= deadline:
                self.fail('未找到{}'.format(description))
            time.sleep(0.5)

    def open_first_hot_video(self):
        def is_hot_video(node):
            name = self.node_name(node)
            return (node.tag == 'XCUIElementTypeOther'
                    and 180 <= float(node.get('y', 0)) < 790
                    and float(node.get('width', 0)) >= 350
                    and float(node.get('height', 0)) >= 80
                    and 'up主' in name and '播放' in name)

        self._tap_first_matching(is_hot_video, '热门页视频卡片')
        self.wait_for('评论', max_y=450)

    def open_first_profile_video(self):
        def is_profile_video_title(node):
            return (node.tag == 'XCUIElementTypeStaticText'
                    and 500 <= float(node.get('y', 0)) < 820
                    and float(node.get('x', 0)) >= 130
                    and float(node.get('width', 0)) >= 170
                    and float(node.get('height', 0)) >= 25)

        self._tap_first_matching(is_profile_video_title, 'UP 主主页的视频')
        self.wait_for('评论', max_y=450)

    def open_search(self):
        self.tap('搜索栏', max_y=120, wait=1)
        self.wait_for('搜索', max_y=120)

    def search(self, text):
        self.enter_text(text, clear=True)
        self.tap('搜索', min_y=40, max_y=130, wait=5)
        self.wait_for('综合', max_y=160)

    def open_search_result_video(self):
        def is_video_title(node):
            name = self.node_name(node)
            return (node.tag == 'XCUIElementTypeStaticText'
                    and 380 <= float(node.get('y', 0)) < 800
                    and float(node.get('width', 0)) >= 140
                    and float(node.get('height', 0)) >= 18
                    and '会员购' not in name)

        self._tap_first_matching(is_video_title, '搜索结果中的视频')
        self.wait_for('评论', max_y=450)

    def open_up_profile(self):
        self.tap('up主头像', wait=4)
        self.wait_for('主页', min_y=350, max_y=550)
        self.wait_for('投稿', min_y=350, max_y=550)

    def open_comments(self):
        self.tap('评论', max_y=450, wait=3)
        self.wait_for('热门评论', '最新评论', contains=True)

    def enter_full_screen(self):
        size = self.device.window_size()
        self.device.click(round(size.width / 2), round(size.height * 0.18))
        time.sleep(0.5)
        # 播放器控件约 3 秒后自动隐藏；抓一遍 source 再点击会错过窗口。
        # 2026-09-10 weditor（402×874）：横屏按钮中心为 (379, 266)。
        self.device.click(size.width - 23, round(size.height * 0.304))
        deadline = time.monotonic() + 6
        while self.device.orientation != 'LANDSCAPE':
            if time.monotonic() >= deadline:
                self.fail('点击全屏按钮后未切换到横屏')
            time.sleep(0.5)

    def type_barrage(self, text):
        size = self.device.window_size()
        self.device.double_tap(round(size.width / 2), round(size.height / 2))
        time.sleep(1)
        if self.find('播放') is None:
            self.fail('双击屏幕后视频未暂停')
        self.tap('bbplayer_fullscreen_dminput',
                 '发个友善的弹幕见证当下文本栏', wait=1)
        nodes = self.nodes()
        if self.find('请转正答题', nodes=nodes) is not None:
            self.fail('当前哔哩哔哩账号尚未转正，无法发送弹幕；请先完成转正答题')
        if self.find('登录', '立即登录', contains=True, nodes=nodes) is not None:
            self.fail('当前哔哩哔哩账号未登录，无法发送弹幕')
        self.enter_text(text, clear=True)

    def send_barrage(self):
        self.tap('发送弹幕', '发送', timeout=6, wait=1)

    def resume_video(self, watch_seconds):
        size = self.device.window_size()
        self.device.double_tap(round(size.width / 2), round(size.height / 2))
        time.sleep(watch_seconds)

    def exit_full_screen(self):
        # 先按模型步骤侧滑；若播放器未响应，再使用 WDA 定位到的返回按钮。
        self.device.swipe(0.01, 0.5, 0.8, 0.5, 0.3)
        time.sleep(2)
        if self.device.orientation == 'LANDSCAPE':
            size = self.device.window_size()
            self.device.click(round(size.width / 2), round(size.height / 2))
            time.sleep(0.5)
            self.tap('bbplayer_fullscreen_back', wait=2)
        if self.device.orientation != 'PORTRAIT':
            self.fail('未退出视频全屏')

    def open_first_live(self):
        def is_live_card(node):
            name = self.node_name(node)
            return (node.tag in ('XCUIElementTypeOther', 'XCUIElementTypeStaticText')
                    and bool(name)
                    and 480 <= float(node.get('y', 0)) < 790
                    and 30 <= float(node.get('x', 0)) < 360
                    and float(node.get('width', 0)) >= 60
                    and 16 <= float(node.get('height', 0)) <= 40
                    and '滚动条' not in name)

        self._tap_first_matching(is_live_card, '直播页的第一个直播')
        self.wait_for('first-line-back-button')

    def enter_live_landscape(self):
        self.tap('live vertical panel fullscreen', wait=3)
        if self.device.orientation != 'LANDSCAPE':
            self.fail('直播未切换到横屏')

    def _is_home(self, nodes):
        return (self.find('搜索栏', nodes=nodes) is not None
                and self.find('首页', contains=True, min_y=740, nodes=nodes) is not None)

    def return_bilibili_home(self):
        for _ in range(8):
            nodes = self.nodes()
            if self._is_home(nodes):
                return
            if self.device.orientation == 'LANDSCAPE':
                back = self.find('bbplayer_fullscreen_back',
                                 'first-line-back-button', nodes=nodes)
                if back is None:
                    size = self.device.window_size()
                    self.device.click(round(size.width / 2), round(size.height / 2))
                    time.sleep(0.5)
                    nodes = self.nodes()
                    back = self.find('bbplayer_fullscreen_back',
                                     'first-line-back-button', nodes=nodes)
                if back is not None:
                    self.tap_node(back)
                else:
                    self.device.swipe(0.01, 0.5, 0.8, 0.5, 0.3)
            else:
                back = self.find('bbplayer_halfscreen_back',
                                 'first-line-back-button', nodes=nodes)
                if back is not None:
                    self.tap_node(back)
                else:
                    self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达哔哩哔哩主界面')
