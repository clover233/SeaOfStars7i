"""汽水音乐动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class SodaMusicCase(WdaCase):
    PACKAGE = 'com.soda.music'
    APP_NAME = '汽水音乐'

    # 2026-09-16 weditor 实测设备尺寸为 402 x 874。播放器中间按钮和
    # 歌单入口均为画布元素，没有稳定的 accessibility 名称。
    PLAYER_BUTTON = (201, 819)
    PLAYLIST_BUTTON = (366, 724)
    SEARCH_BUTTON = (369, 84)

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
            logging.exception('结束汽水音乐进程失败，继续尝试启动')
        time.sleep(1)

    def wait_for(self, *names, timeout=10, contains=False, min_y=None,
                 max_y=None):
        deadline = time.monotonic() + timeout
        while True:
            node = self.find(*names, contains=contains, min_y=min_y,
                             max_y=max_y)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('等待控件超时：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def fail_if_security_verification(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('验证码', nodes=nodes) is not None or
                self.find('请完成下列验证后继续', nodes=nodes) is not None):
            self.fail('触发汽水音乐滑块验证码，请先人工完成验证再运行')

    def dismiss_optional_prompts(self):
        """关闭普通引导；激励广告和验证码要求人工预处理。"""
        for _ in range(6):
            nodes = self.nodes()
            self.fail_if_security_verification(nodes)

            known = self.find('我知道了', nodes=nodes)
            if known is not None:
                self.tap_node(known)
                time.sleep(2)
                continue

            exit_ad = self.find('坚持退出', nodes=nodes)
            if exit_ad is not None:
                self.tap_node(exit_ad)
                time.sleep(2)
                continue

            if self.find('再看1个享全天免费听', contains=True,
                         nodes=nodes) is not None:
                # 奖励弹层右上角 X 未暴露给 WDA。
                self.device.click(359, 490)
                time.sleep(2)
                continue

            if self.find('新客专属优惠', contains=True, nodes=nodes) is not None:
                # 点击弹层外侧关闭，不能点“免费听歌”，否则会进入激励广告。
                self.device.click(201, 200)
                time.sleep(2)
                continue

            if (self.find('立即下载', nodes=nodes) is not None and
                    self.find('向上滑动浏览落地页', nodes=nodes) is not None):
                self.fail('启动时仍停留在激励广告，请先人工关闭广告再运行')
            visible_named = [node for node in nodes
                             if node.get('visible') == 'true'
                             and self.node_name(node)]
            if (len(visible_named) <= 2 and
                    self.find('lynxview', nodes=nodes) is not None and
                    self.find('标签页栏', nodes=nodes) is None):
                self.fail('汽水音乐显示全屏激励广告，请先人工等待并关闭广告')
            return

    def start_sodamusic(self):
        self.start_app(wait=4)
        self.dismiss_optional_prompts()
        self.return_home()

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            # 当前版本“发现”是推荐网格；带底部播放键的主界面对应中间
            # song/音乐 Tab。Excel 中的“首页”按播放器主界面处理。
            player_tab = self.find('song', min_y=760, nodes=nodes)
            if player_tab is not None:
                self.tap_node(player_tab)
                time.sleep(3)
                self.dismiss_optional_prompts()
                landed = self.nodes()
                if (self.find('play_comment_button', nodes=landed) is not None
                        or self.find('模式选择', nodes=landed) is not None):
                    return
                continue
            cancel = self.find('取消', max_y=130, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(3)
                continue
            back = self.find('返回', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
                continue
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
            time.sleep(3)
        self.fail('多次返回后仍未到达汽水音乐主界面')

    def open_search(self):
        self.return_home()
        grid_search = self.find('搜索歌手、歌曲或专辑名', contains=True,
                                max_y=150)
        if grid_search is not None:
            self.tap_node(grid_search)
            time.sleep(3)
        else:
            # 播放器页右上角放大镜是画布元素，weditor 实测中心点 (369, 84)。
            self.device.click(*self.SEARCH_BUTTON)
            time.sleep(3)
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeTextField']
        if not fields:
            self.fail('点击搜索图标后未进入搜索页')

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        # 输入后优先选择完全匹配的联想词，比不同输入法的 Search 键稳定。
        suggestion = self.find(keyword, min_y=110, max_y=540)
        if suggestion is not None:
            self.tap_node(suggestion)
        else:
            self.tap('Search', '搜索', min_y=700, wait=1)
        time.sleep(6)
        self.fail_if_security_verification()
        if self.find('综合', max_y=180) is None:
            self.fail('搜索后未进入“{}”结果页'.format(keyword))

    def _player_is_playing(self):
        """通过无障碍树缺失的播放/暂停图标中心像素判断状态。"""
        image = self.device.screenshot().convert('RGB')
        width, height = self.device.window_size()
        x = round(self.PLAYER_BUTTON[0] * image.width / width)
        y = round(self.PLAYER_BUTTON[1] * image.height / height)
        pixel = image.getpixel((x, y))
        # 播放态显示“暂停”双竖线，按钮正中心为深色；暂停态显示白色三角。
        return sum(pixel) / 3 < 128

    def _wait_player_state(self, playing, timeout=4):
        deadline = time.monotonic() + timeout
        while True:
            if self._player_is_playing() == playing:
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.5)

    def play_for_15_seconds_and_pause(self):
        self.return_home()
        if self._player_is_playing():
            for _ in range(2):
                self.device.click(*self.PLAYER_BUTTON)
                if self._wait_player_state(False):
                    break
        if not self._wait_player_state(False, timeout=1):
            self.fail('无法将首页播放器切换到暂停态')

        started_at = time.monotonic()
        self.device.click(*self.PLAYER_BUTTON)
        if not self._wait_player_state(True):
            self.fail('点击播放按钮后音乐未开始播放')
        time.sleep(max(0, 15 - (time.monotonic() - started_at)))
        self.device.click(*self.PLAYER_BUTTON)
        if not self._wait_player_state(False):
            self.fail('播放15秒后未能暂停音乐')

    def open_mine(self):
        self.tap('mine', min_y=760, wait=4)
        self.dismiss_optional_prompts()
        self.wait_for('我喜欢的音乐', timeout=8)

    def open_liked_music(self):
        self.tap('我喜欢的音乐', wait=4)
        self.wait_for('我喜欢的音乐', timeout=8)

    def open_playlist(self):
        self.return_home()
        # 当前歌曲右侧竖向省略号不在 WDA 树中。
        self.device.click(*self.PLAYLIST_BUTTON)
        time.sleep(4)
        self.wait_for('返回', max_y=130, timeout=8)

    def close_playlist(self):
        self.tap('返回', max_y=130, wait=4)
        self.return_home()
