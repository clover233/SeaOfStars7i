"""网易云音乐动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class CloudMusicCase(WdaCase):
    PACKAGE = 'com.netease.cloudmusic'
    APP_NAME = '网易云音乐'

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

    def _dismiss_vip_popup(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        interrupted = self.find('播放被其他应用或系统打断', nodes=nodes)
        if interrupted is not None:
            self.tap('知道了', '我知道了', wait=1)
            return True
        trial = next((node for node in self.matching_nodes(
            '开通VIP听整首', contains=True, nodes=nodes)
            if node.tag == 'XCUIElementTypeStaticText'), None)
        if trial is not None:
            # 试听弹层：无标签 X 位于试听文案左上方一行的右端。
            size = self.device.window_size()
            self.device.click(size.width - 29, round(float(trial.get('y', 0)) - 21))
            time.sleep(2)
            return True
        ended = self.find('免费听歌模式已结束', nodes=nodes)
        if ended is not None:
            # 430×932 实机：无标签 X 与标题顶边同高，位于弹层右上角。
            size = self.device.window_size()
            self.device.click(round(size.width * 0.91), round(float(ended.get('y', 0))))
            time.sleep(2)
            return True
        offers = self.matching_nodes('喜欢这首歌？喜欢可以下载TA',
                                     contains=True, min_y=200, nodes=nodes)
        if offers:
            # 当前优惠弹层的标题仅作为整个 WebView 容器的名称暴露。
            # 容器左上角为 (0,448)，无标签关闭按钮中心 (401,477)。
            panel = offers[0]
            size = self.device.window_size()
            self.device.click(size.width - 29, round(float(panel.get('y', 0)) + 29))
            time.sleep(2)
            return True
        popup = self.find('您的黑胶VIP权益即将过期', contains=True, nodes=nodes)
        if popup is None:
            return False
        # 2026-09-10 weditor（402×874）：弹层 X 未暴露可访问名，中心 (373, 472)。
        size = self.device.window_size()
        self.device.click(size.width - 29, round(size.height * 0.54))
        time.sleep(3)
        return True

    def _is_player(self, nodes):
        return (self.find('NMPlayView', nodes=nodes) is not None
                or self.find('下一首', nodes=nodes) is not None)

    def return_home(self):
        for _ in range(8):
            nodes = self.nodes()
            if self._dismiss_vip_popup(nodes):
                continue
            if (self.find('我的消息', contains=True, nodes=nodes) is not None
                    and self.find('设置', nodes=nodes) is not None):
                # 旧的左边缘右滑会打开侧栏；点击侧栏外的遮罩关闭。
                size = self.device.window_size()
                self.device.click(round(size.width * 0.95), round(size.height * 0.4))
                time.sleep(2)
                continue
            home = self.find('首页', min_y=740, nodes=nodes)
            recommendation = self.find('推荐', max_y=150, nodes=nodes)
            if home is not None and recommendation is not None:
                self.tap_node(home)
                time.sleep(2)
                self.tap('推荐', max_y=150, wait=5)
                self._find_playlist_section()
                return
            if self._is_player(nodes):
                back = self.find('返回', 'modern_playview_navigator_fold',
                                 max_y=140, nodes=nodes)
                if back is not None:
                    self.tap_node(back)
                else:
                    self.device.click(33, 78)
            else:
                self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达网易云音乐首页')

    def start_cloudmusic(self):
        self.start_app(wait=6)
        self.return_home()

    def browse_home(self):
        for _ in range(2):
            for start, end in ((0.75, 0.35), (0.75, 0.35),
                               (0.35, 0.75), (0.35, 0.75)):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        time.sleep(1)

    def _find_playlist_section(self):
        for names, start, end in ((('雷达歌单',), 0.75, 0.4),
                                  (('雷达歌单', '推荐歌单'), 0.35, 0.75)):
            for _ in range(6):
                nodes = self.nodes()
                # 顶部快捷入口也叫“雷达歌单”，只有左对齐的区块标题
                # 才对应其下方的歌单卡片。
                sections = [node for node in self.matching_nodes(
                    *names, contains=True, nodes=nodes)
                    if node.tag == 'XCUIElementTypeStaticText'
                    and float(node.get('x', 0)) <= 40]
                if sections:
                    section = sections[0]
                    if float(section.get('y', 0)) > self.device.window_size().height * 0.6:
                        self.device.swipe(0.5, 0.7, 0.5, 0.4, 0.3)
                        time.sleep(1)
                        continue
                    return nodes, section
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        self.fail('首页未找到“雷达歌单”或“推荐歌单”')

    def open_first_playlist(self):
        nodes, section = self._find_playlist_section()
        section_name = self.node_name(section)
        if '雷达歌单' not in section_name:
            logging.warning('当前网易云音乐已无“雷达歌单”，使用“推荐歌单”第一条替代')
        section_y = float(section.get('y', 0))
        candidates = []
        for node in nodes:
            x = float(node.get('x', 0))
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            height = float(node.get('height', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and x < 170 and width >= 100 and height >= 20
                    and section_y + 50 < y < section_y + 260):
                candidates.append(node)
        if not candidates:
            self.fail('{}下未找到第一个歌单'.format(section_name))
        candidates.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(candidates[0])
        time.sleep(6)
        self.wait_for('播放全部', contains=True)

    def _show_player_controls(self):
        nodes = self.nodes()
        for _ in range(3):
            if not self._dismiss_vip_popup(nodes):
                break
            nodes = self.nodes()
        if self.find('下一首', nodes=nodes) is None:
            size = self.device.window_size()
            self.device.click(round(size.width / 2), round(size.height * 0.49))
            time.sleep(1)
        return self.wait_for('下一首', timeout=5)

    def play_all(self):
        self.tap('播放全部', contains=True, wait=4)
        deadline = time.monotonic() + 15
        while True:
            nodes = self.nodes()
            if self._dismiss_vip_popup(nodes):
                continue
            if self._is_player(nodes):
                self._show_player_controls()
                return
            cover = self.find('minibar_song_cover_floating', nodes=nodes)
            if cover is not None:
                self.tap_node(cover)
                time.sleep(3)
                continue
            if time.monotonic() >= deadline:
                self.fail('点击“播放全部”后未进入播放页')
            time.sleep(0.5)

    def next_tracks(self, count):
        for _ in range(count):
            next_button = self._show_player_controls()
            self.tap_node(next_button)
            time.sleep(1)

    def pause_playback(self):
        self._show_player_controls()
        nodes = self.nodes()
        pause = self.find('暂停', nodes=nodes)
        if pause is None:
            self.fail('播放页未找到暂停键')
        self.tap_node(pause)
        self.wait_for('播放', timeout=5)
