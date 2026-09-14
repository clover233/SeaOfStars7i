"""抖音极速版动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class DouyinJisuCase(WdaCase):
    PACKAGE = 'com.ss.iphone.ugc.aweme.lite'
    APP_NAME = '抖音极速版'

    def _enable_continuous_ui_mode(self):
        """避免视频持续刷新让 XCTest 一直等待应用进入 idle。"""
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

    def _dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '我知道了', '取消', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_douyin(self):
        self._enable_continuous_ui_mode()
        self.start_app(wait=7)
        self._dismiss_optional_prompts()
        nodes = self.nodes()
        home = self.find('首页', min_y=740, nodes=nodes)
        if home is not None:
            self.tap_node(home)
            time.sleep(3)

    def open_recommend(self):
        self.tap('推荐', max_y=140, wait=4)

    def browse_recommend(self):
        self.browse(5, 5)

    def open_hotspot(self):
        hotspot = None
        # “热点”在顶部横向栏目靠左位置；推荐页默认可能把它滚出可视区。
        # 2026-09-11 weditor（402×874）：手势必须从栏目内部起滑，避开侧边栏。
        for _ in range(6):
            nodes = self.nodes()
            hotspot = self.find('热点', max_y=140, nodes=nodes)
            if hotspot is not None:
                break
            self.device.swipe(140, 84, 330, 84, 0.5)
            time.sleep(1)
        if hotspot is None:
            nodes = self.nodes()
            hotspot = self.find('同城', max_y=140, nodes=nodes)
            if hotspot is None:
                self.fail('当前版本未找到“热点”或可替代的“同城”入口')
            logging.warning('顶部栏目滑到最左侧仍无“热点”，使用“同城”视频流替代')
        self.tap_node(hotspot)
        time.sleep(5)
        self._dismiss_optional_prompts()

    def play_first_video(self):
        nodes = self.nodes()
        if self.find('评论', contains=True, nodes=nodes) is not None:
            logging.info('第一条视频已在视频流中自动播放')
            return
        hot_items = [node for node in nodes
                     if node.get('visible') == 'true'
                     and self.node_name(node).startswith('热点榜:')]
        if hot_items:
            # 热点首页先展示热榜词条；进入第一条词条后，再点首个视频卡片。
            self.tap_node(sorted(hot_items, key=lambda item: float(
                item.get('y', 0)))[0])
            time.sleep(6)
            # 搜索结果横向视频卡片由 Lynx 自绘，WDA 只暴露整个 CollectionView。
            # 2026-09-11 weditor（402×874）：第一张视频卡片中心区域。
            self.device.click(120, 300)
            time.sleep(7)
            return
        cards = []
        for node in nodes:
            if node.get('visible') != 'true':
                continue
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.tag in ('XCUIElementTypeCell', 'XCUIElementTypeOther')
                    and y > 130 and width > 150 and height > 150):
                cards.append(node)
        if cards:
            self.tap_node(sorted(cards, key=lambda item: (
                float(item.get('y', 0)), float(item.get('x', 0))))[0])
        else:
            self.device.click(100, 300)
        time.sleep(5)

    def open_author(self):
        nodes = self.nodes()
        author = None
        for node in nodes:
            name = self.node_name(node)
            y = float(node.get('y', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and name.startswith('@') and 200 < y < 760):
                author = node
                break
        if author is None:
            logging.warning('作者名称未暴露给 WDA，使用作者头像坐标')
            self.device.click(352, 360)
        else:
            self.tap_node(author)
        time.sleep(6)
        if self.find('返回', max_y=140) is None:
            self.fail('点击作者后未进入 UP 主主页')

    def browse_author(self):
        self.browse(5, 5)

    def open_first_author_video(self):
        nodes = self.nodes()
        candidates = []
        for node in nodes:
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeOther', 'XCUIElementTypeCell')
                    and y > 430 and width >= 110 and height >= 130):
                candidates.append(node)
        if candidates:
            self.tap_node(sorted(candidates, key=lambda item: (
                float(item.get('y', 0)), float(item.get('x', 0))))[0])
        else:
            logging.warning('UP 主作品宫格未暴露给 WDA，使用首个作品坐标')
            self.device.click(68, 590)
        time.sleep(6)

    def open_comments(self):
        # 2026-09-11 weditor（402×874）：播放器评论按钮位于右侧中部。
        self.device.click(372, 530)
        time.sleep(5)

    def return_main(self):
        self.device.swipe(0.5, 0.35, 0.5, 0.9, 0.3)
        time.sleep(2)
        for _ in range(3):
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(3)
            nodes = self.nodes()
            home = self.find('首页', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                self._restore_idle_settings()
                return
        self._restore_idle_settings()
        self.fail('未返回抖音极速版主界面')
