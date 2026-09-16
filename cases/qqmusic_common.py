"""QQ 音乐动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class QqMusicCase(WdaCase):
    PACKAGE = 'com.tencent.QQMusic'
    APP_NAME = 'QQ音乐'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾维测打点至少覆盖 xctrace 的 5 秒采样窗口。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self, terminate=True):
        if terminate:
            try:
                self.device.app_terminate(self.PACKAGE)
            except Exception:
                logging.exception('结束QQ音乐进程失败，继续尝试启动')
            time.sleep(1)

    def dismiss_optional_prompts(self):
        for _ in range(8):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '暂不', '我知道了', '关闭按钮',
                '跳过', nodes=nodes,
            )
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_qqmusic(self, normalize_home=True):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        if normalize_home:
            self.return_music_home()

    def browse_music(self, up, down):
        # QQ音乐的 Charts/乐馆页面对通用坐标 swipe 不稳定，WDA 的
        # swipe_up/swipe_down 能稳定命中实际滚动容器。
        for _ in range(up):
            self.device.swipe_up()
            time.sleep(1)
        for _ in range(down):
            self.device.swipe_down()
            time.sleep(1)
        time.sleep(1)

    def return_music_home(self):
        for _ in range(10):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            home = self.find('首页', min_y=780, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                recommend = self.find('推荐', max_y=180)
                if recommend is not None:
                    self.tap_node(recommend)
                    time.sleep(2)
                return
            close = self.find('关闭', min_y=740, nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(3)
                continue
            hide = self.find('隐藏正在播放界面', max_y=130, nodes=nodes)
            if hide is not None:
                self.tap_node(hide)
                time.sleep(3)
                continue
            cancel = self.find('取消', max_y=150, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(3)
                continue
            back = self.find('返回', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
                continue
            self.device.swipe(4, 437, 354, 437, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达QQ音乐首页')

    def open_mine(self):
        self.tap('我的', min_y=780, wait=4)
        self.dismiss_optional_prompts()
        if self.find('最近播放', contains=True) is None:
            self.fail('未进入QQ音乐“我的”页面')

    def open_recent(self):
        self.tap('mymusic_channelMoreBtnIcon_v20', wait=4)
        self.dismiss_optional_prompts()
        if self.find('最近播放', max_y=130) is None:
            self.fail('未进入最近播放页面')

    def back(self):
        self.tap('返回', max_y=130, wait=3)

    def open_local(self):
        self.tap('本地 ', '本地', contains=True, min_y=300, max_y=480, wait=4)
        # 首次进入会出现媒体资料库权限；此用例只验证页面进入，拒绝权限
        # 也能完成步骤，且不会修改系统隐私授权为“允许”。
        self.dismiss_optional_prompts()
        if self.find('本地歌曲', max_y=140) is None:
            self.fail('未进入本地歌曲页面')

    def open_search_box(self):
        nodes = self.nodes()
        search = self.find('搜索背景控件', nodes=nodes)
        if search is None:
            fields = [node for node in nodes
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeSearchField'
                      and float(node.get('y', 0)) < 130]
            search = fields[0] if fields else None
        if search is None:
            self.fail('QQ音乐首页未找到搜索框')
        self.tap_node(search)
        time.sleep(3)
        if not any(node.get('visible') == 'true'
                   and node.tag == 'XCUIElementTypeTextField'
                   for node in self.nodes()):
            # 2026-09-15 weditor（402×874）：搜索页外层命中偶尔只刷新
            # 热词，点输入区域中部可稳定聚焦键盘。
            self.device.click(170, 88)
            time.sleep(2)

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        self.tap('Search', '搜索', min_y=700, wait=7)
        if self.find('综合', max_y=180) is None:
            self.fail('搜索后未进入综合结果页')

    def switch_result_tab(self, name):
        self.tap(name, max_y=180, wait=3)

    def play_first_search_result(self, keyword, seconds=20):
        nodes = self.nodes()
        matches = self.matching_nodes(
            keyword, min_y=450, max_y=760, nodes=nodes)
        if not matches:
            self.fail('搜索结果中未找到歌曲：{}'.format(keyword))
        self.tap_node(matches[0])
        time.sleep(4)
        self.ensure_player_detail()
        time.sleep(max(0, seconds - 4))

    def ensure_player_detail(self):
        if self.find('隐藏正在播放界面', max_y=130) is not None:
            return
        nodes = self.nodes()
        minibar = [node for node in nodes
                   if node.get('visible') == 'true'
                   and 730 <= float(node.get('y', 0)) <= 830
                   and float(node.get('width', 0)) >= 180
                   and node.tag == 'XCUIElementTypeOther']
        if not minibar:
            self.fail('歌曲已播放，但未找到底部正在播放卡片')
        self.tap_node(minibar[0])
        time.sleep(4)
        if self.find('隐藏正在播放界面', max_y=130) is None:
            self.fail('未进入歌曲播放详情页')

    def pause_player(self):
        self.tap('暂停', min_y=700, wait=3)

    def favorite_then_unfavorite(self):
        already = self.find('已收藏', min_y=430, max_y=560)
        if already is not None:
            self.tap_node(already)
            time.sleep(2)
        self.tap('收藏', min_y=430, max_y=560, wait=2)
        self.tap('已收藏', min_y=430, max_y=560, wait=2)

    def lyrics_round_trip(self):
        self.device.swipe_left()
        time.sleep(3)
        self.device.swipe_right()
        time.sleep(3)

    def open_rankings(self):
        self.return_music_home()
        self.tap('乐馆', max_y=180, wait=5)
        # 2026-09-15 weditor（402×874）：乐馆二级“排行”由画布绘制，
        # 没有稳定 accessibility 节点。
        self.tap('排行', '排行榜', fallback=(126, 111), max_y=180, wait=6)
        if self.find('Charts', max_y=220) is None:
            self.fail('未进入排行榜 Charts 页面')

    def open_chart(self, name):
        for _ in range(5):
            node = self.find(name, min_y=100, max_y=760)
            if node is not None:
                self.tap_node(node)
                time.sleep(5)
                return
            self.device.swipe_up()
            time.sleep(2)
        self.fail('排行榜页面未找到{}'.format(name))

    def play_first_home_card(self):
        nodes = self.nodes()
        play_buttons = self.matching_nodes(
            '播放', min_y=150, max_y=700, nodes=nodes)
        if not play_buttons:
            self.fail('首页未找到可播放的音乐卡片')
        self.tap_node(play_buttons[0])
        time.sleep(5)
        if self.find('暂停', min_y=700) is None:
            self.fail('点击音乐卡片后未开始播放')

    def pause_miniplayer(self):
        pause = self.find('暂停', min_y=700)
        if pause is None:
            self.fail('底部播放器当前不是播放状态；请先运行qqm_0040或预置一首正在播放的歌曲')
        self.tap_node(pause)
        time.sleep(3)
