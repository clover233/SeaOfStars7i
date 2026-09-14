"""红果免费短剧动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class HongguoCase(WdaCase):
    PACKAGE = 'com.phoenix.video'
    APP_NAME = '红果免费短剧'

    def _enable_continuous_ui_mode(self):
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings({
                'waitForIdleTimeout': 0,
                'animationCoolOffTimeout': 0,
            })
        except Exception:
            logging.exception('WDA 不支持 idle 等待设置，继续使用默认配置')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is None:
            return
        try:
            self.device.appium_settings(previous)
        except Exception:
            logging.exception('恢复 WDA idle 等待设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束红果免费短剧进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

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

    def _dismiss_optional_prompts(self):
        for _ in range(5):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '暂不', '我知道了',
                'widget guide close', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def _edge_back(self):
        if self.device.orientation == 'LANDSCAPE':
            self.device.click(437, 201)
            time.sleep(1)
            self.device.click(108, 45)
        else:
            self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(2)

    def start_hongguo(self):
        self.start_app(wait=5)
        self._dismiss_optional_prompts()
        self.return_home_feed()

    def return_home_feed(self):
        for _ in range(10):
            nodes = self.nodes()
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                return
            self._edge_back()
        self.fail('多次返回后仍未到达红果首页')

    def swipe_vertical(self, up, down):
        for start, end, count in ((650, 300, up), (300, 650, down)):
            for _ in range(count):
                self.device.swipe(201, start, 201, end, 0.3)
                time.sleep(1)
        time.sleep(1)

    def open_theatre(self):
        self.tap('剧场', min_y=760, wait=4)
        self._dismiss_optional_prompts()
        self.wait_for('排行榜', max_y=230, timeout=10)

    def open_ranking(self):
        self.tap('排行榜', max_y=230, wait=4)
        self.wait_for('推荐榜', max_y=300, timeout=10)

    def open_first_ranking_card(self):
        nodes = self.nodes()
        cards = []
        for node in nodes:
            _, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and 250 <= y <= 760 and width >= 300 and height >= 80):
                cards.append(node)
        if cards:
            cards.sort(key=lambda node: float(node.get('y', 0)))
            self.tap_node(cards[0])
        else:
            logging.warning('排行榜首条卡片未暴露名称，使用 weditor 核对坐标')
            self.device.click(201, 330)
        time.sleep(5)

    def return_from_video(self):
        self._edge_back()
        self.wait_for('推荐榜', '热播榜', max_y=300, timeout=10)

    def return_to_theatre(self):
        for _ in range(4):
            nodes = self.nodes()
            theatre = self.find('剧场', min_y=760, nodes=nodes)
            if theatre is not None:
                self.tap_node(theatre)
                time.sleep(3)
                return
            back = self.find('返回键', max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self._edge_back()
        self.fail('未能返回红果剧场界面')

    def open_my(self):
        self.tap('我的', min_y=760, wait=4)
        self.wait_for('历史', max_y=500, timeout=10)

    def long_press_speed(self):
        self.device.tap_hold(201, 400, 1.5)
        time.sleep(2)
        self.wait_for('倍速', timeout=8)
        self.tap('2x', '2.0x', wait=3)

    def open_comments(self):
        self.tap('short_video_comment_icon', wait=3)
        self.wait_for('community short video close', timeout=8)

    def close_comments_by_edge(self):
        self.device.swipe(4, 520, 354, 520, 0.3)
        time.sleep(3)

    def follow_current_drama(self):
        nodes = self.nodes()
        followed = self.find('short_video_stared_icon_663', nodes=nodes)
        if followed is not None:
            logging.info('当前短剧已在追剧列表，无需反向取消')
            return
        star = self.find('short_video_star_icon_663', nodes=nodes)
        if star is None:
            self.fail('未找到追剧按钮')
        self.tap_node(star)
        time.sleep(2)

    def leave_player_to_feed(self):
        self._edge_back()
        self.wait_for('首页', min_y=760, timeout=10)

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        self.tap('搜索', max_y=130, wait=5)
        nodes = self.nodes()
        keyboard_search = self.find('Search', min_y=700, nodes=nodes)
        if keyboard_search is not None:
            self.tap_node(keyboard_search)
            time.sleep(5)
        self.wait_for('综合', '剧集', max_y=180, timeout=12)

    def open_first_search_result(self):
        deadline = time.monotonic() + 12
        while True:
            nodes = self.nodes()
            heats = [node for node in nodes
                     if node.get('visible') == 'true'
                     and '热度' in self.node_name(node)
                     and 180 <= float(node.get('y', 0)) <= 700]
            if heats:
                heats.sort(key=lambda node: (
                    float(node.get('y', 0)), float(node.get('x', 0))))
                y = round(float(heats[0].get('y', 0)) + 35)
                self.device.click(100, min(y, 730))
                time.sleep(5)
                self.wait_for('全屏观看', timeout=10)
                return
            if time.monotonic() >= deadline:
                self.fail('搜索结果中未找到第一条短剧')
            time.sleep(0.5)

    def enter_fullscreen(self):
        self.tap('全屏观看', wait=3)
        deadline = time.monotonic() + 8
        while self.device.orientation != 'LANDSCAPE':
            if time.monotonic() >= deadline:
                self.fail('视频未切换到横屏播放')
            time.sleep(0.5)

    def return_search_video_to_theatre(self):
        if self.device.orientation == 'LANDSCAPE':
            self._edge_back()
        # 竖屏详情 -> 搜索结果 -> 搜索首页 -> 剧场。
        for _ in range(3):
            self._edge_back()
        self.wait_for('剧场', min_y=760, timeout=12)
