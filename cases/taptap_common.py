"""TapTap 动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class TapTapCase(WdaCase):
    PACKAGE = 'com.easyplay.taptap.now'
    APP_NAME = 'TapTap'

    def _dismiss_tracking_prompt(self):
        nodes = self.nodes()
        button = self.find('要求App不跟踪', nodes=nodes)
        if button is not None:
            self.tap_node(button)
            time.sleep(5)

    def start_taptap(self):
        self.start_app(wait=7)
        self._dismiss_tracking_prompt()
        self.return_find_games()

    def return_find_games(self):
        for _ in range(7):
            nodes = self.nodes()
            home = self.find('找游戏', min_y=780, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                return
            back = self.find('BackButton', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(3)
        self.fail('未返回 TapTap 找游戏页')

    def search_game(self, text):
        self.tap('搜索', min_y=760, wait=3)
        if not self.matching_nodes('search.voice.input'):
            self.fail('TapTap 搜索页未找到搜索框')
        element = self.device(className='XCUIElementTypeSearchField')
        try:
            element.clear_text()
        except Exception:
            logging.info('TapTap 搜索框当前为空，无需清除')
        element.set_text(text + '\n')
        time.sleep(7)

    def open_first_result(self, text):
        self.tap(text, min_y=130, max_y=300, wait=7)
        if self.find(text, min_y=120, max_y=230) is None:
            self.fail('未进入{}游戏详情'.format(text))

    def open_reviews(self):
        for _ in range(5):
            nodes = self.nodes()
            targets = [node for node in nodes
                       if node.get('visible') == 'true'
                       and self.node_name(node).startswith('共 ')
                       and self.node_name(node).endswith('条')]
            if targets:
                self.tap_node(targets[0])
                time.sleep(6)
                if self.find('玩家点评', contains=True) is not None:
                    return
            self.device.swipe(0.5, 0.72, 0.5, 0.38, 0.3)
            time.sleep(2)
        self.fail('王者荣耀详情未找到全部评价入口')

    def open_tab(self, name):
        self.return_find_games()
        self.tap(name, min_y=760, wait=6)

    def open_my_games(self):
        nodes = self.nodes()
        avatar = self.find('TapTap.Profile.CurrentUser.Avatar', nodes=nodes)
        if avatar is None:
            self.fail('当前页面未找到 TapTap 个人头像入口')
        self.tap_node(avatar)
        time.sleep(6)
        self.tap('查看全部', wait=5)
        if self.find('游戏时长') is None:
            self.fail('未进入“我的游戏”页面')

    def open_personal_profile(self):
        nodes = self.nodes()
        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeStaticText'
                      and 170 <= float(node.get('y', 0)) <= 230]
        if candidates:
            self.tap_node(candidates[0])
            time.sleep(5)
        nodes = self.nodes()
        if self.find('ID:', contains=True, nodes=nodes) is None:
            logging.warning('“我的游戏”页昵称不可点击，侧滑返回个人主页')
            back = self.find('BackButton', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(5)
        if self.find('ID:', contains=True) is None:
            self.fail('未进入 TapTap 个人主页')
