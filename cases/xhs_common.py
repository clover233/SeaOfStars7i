"""小红书 iOS 动态性能用例公共能力。"""

import logging
import re
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class XhsCase(WdaCase):
    PACKAGE = 'com.xingin.discover'
    APP_NAME = '小红书'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只采集首尾步骤，并保证每段 trace 不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置小红书连续页面模式失败')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is not None:
            try:
                self.device.appium_settings(previous)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束小红书进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭不影响测试的更新、通知、跟踪和运营弹窗。"""
        for _ in range(5):
            nodes = self.nodes()
            names = [self.node_name(node) for node in nodes]
            if any(('照片' in name or '相册' in name) and any(word in name for word in (
                    '允许', '访问', '权限', '设置中开启')) for name in names):
                self.fail('请先在系统设置中授予小红书照片访问权限')
            button = self.find(
                '要求App不跟踪', '要求 App 不跟踪', '不允许', '以后再说',
                '下次再说', '暂不开启', '暂不更新', '我知道了', '稍后',
                '跳过', '关闭', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        has_home_tab = self.find('首页', min_y=760, nodes=nodes) is not None
        has_feed_tabs = all(self.find(name, max_y=130, nodes=nodes) is not None
                            for name in ('关注', '发现', '同城'))
        return has_home_tab and has_feed_tabs

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_home(nodes):
                return
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                continue
            close = self.find('close', '取消', '返回', max_y=180, nodes=nodes)
            if close is not None:
                self.tap_node(close)
            else:
                self.device.swipe(0.01, 0.5, 0.90, 0.5, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达小红书首页')

    def start_xhs(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()

    def tap_bottom_tab(self, *names, wait=4):
        self.tap(*names, min_y=760, choose='last', wait=wait)

    def open_profile(self):
        self.tap_bottom_tab('我')

    def open_collection(self):
        self.tap('收藏', max_y=460, wait=4)

    def _image_nodes(self, nodes=None, min_y=100):
        nodes = self.nodes() if nodes is None else nodes
        return sorted([
            node for node in nodes
            if node.get('visible') == 'true'
            and node.tag == 'XCUIElementTypeImage'
            and float(node.get('y', 0)) >= min_y
            and float(node.get('width', 0)) >= 150
            and float(node.get('height', 0)) >= 150
        ], key=lambda node: (float(node.get('y', 0)), float(node.get('x', 0))))

    def open_first_collection_note(self):
        images = self._image_nodes(min_y=390)
        if images:
            self.tap_node(images[0])
        else:
            self.device.click(100, 520)
        time.sleep(6)
        self.require_note_detail()

    def open_collected_video(self):
        for _ in range(6):
            nodes = self.nodes()
            marker = next((node for node in nodes
                           if node.get('visible') == 'true'
                           and (re.fullmatch(r'\d+:\d+', self.node_name(node))
                                or 'video' in self.node_name(node).lower())), None)
            if marker is not None:
                x = float(marker.get('x', 0))
                y = float(marker.get('y', 0))
                column_x = 67 if x < 134 else 201 if x < 268 else 335
                self.device.click(column_x, round(max(450, y - 90)))
                time.sleep(7)
                self.require_note_detail()
                return
            self.browse(1, 0)
        self.fail('收藏页未找到带时长标记的视频，请先收藏至少一条视频')

    def require_note_detail(self):
        nodes = self.nodes()
        if self.find('评论输入框', min_y=700, nodes=nodes) is None:
            self.fail('点击内容后未进入笔记详情页')

    def toggle_like(self):
        self.tap('点赞', '已点赞', min_y=700, wait=2)

    def open_comments(self):
        self.tap('评论', min_y=700, wait=4)

    def edge_back(self, wait=3):
        self.device.swipe(0.01, 0.5, 0.90, 0.5, 0.3)
        time.sleep(wait)

    def return_profile(self):
        for _ in range(4):
            nodes = self.nodes()
            if (self.find('菜单', max_y=150, nodes=nodes) is not None and
                    self.find('收藏', max_y=460, nodes=nodes) is not None):
                return
            back = self.find('返回', max_y=150, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.edge_back()
            time.sleep(3)
        self.fail('未返回小红书个人页')

    def open_settings(self):
        self.tap('菜单', max_y=150, wait=3)
        self.tap('设置', contains=True, wait=4)

    def return_from_settings_to_home(self):
        self.return_home()

    def open_first_feed_note(self):
        images = self._image_nodes(min_y=100)
        if images:
            self.tap_node(images[0])
        else:
            self.device.click(100, 260)
        time.sleep(6)
        self.require_note_detail()

    def open_photo_picker(self):
        self.tap('发布标签', min_y=760, wait=3)
        self.tap('从相册选择', fallback=(201, 597), wait=6)
        self.dismiss_optional_prompts()
        if self.find('最近项目', max_y=130) is None:
            self.fail('未进入小红书照片选择页面')

    def open_first_photo_preview(self):
        # 选择圆点位于右上角；点击首格中央可直接打开大图预览。
        self.device.click(67, 210)
        time.sleep(5)

    def horizontal_browse(self, left, right):
        for start, end, count in ((0.86, 0.14, left), (0.14, 0.86, right)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.35)
                time.sleep(1)
        time.sleep(1)

    def open_search(self):
        # 当前版本首页搜索按钮没有 accessibility name。
        self.device.click(376, 82)
        time.sleep(4)
        if self.find('recommend_search_button', '搜索', max_y=130) is None:
            self.fail('未进入小红书搜索页')

    def set_search_text(self, keyword):
        self.enter_text(keyword, clear=True)

    def submit_search(self):
        self.tap('recommend_search_button', '搜索', max_y=130,
                 choose='last', wait=6)

    def search_keyword(self, keyword):
        self.set_search_text(keyword)
        self.submit_search()

    def repeat_search_and_return(self, keyword, count):
        for _ in range(count):
            self.search_keyword(keyword)
            self.edge_back(wait=4)

    def open_first_search_result(self):
        images = self._image_nodes(min_y=180)
        if images:
            self.tap_node(images[0])
        else:
            self.device.click(100, 370)
        time.sleep(6)
        self.require_note_detail()

    def open_note_image_viewer(self):
        self.device.click(201, 350)
        time.sleep(4)

    def open_first_hot_search(self):
        nodes = self.nodes()
        excluded = ('猜你想搜', '搜索发现', '按住提问 有问必答', '搜索')
        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeStaticText'
                      and 140 <= float(node.get('y', 0)) <= 420
                      and self.node_name(node) not in excluded]
        if candidates:
            self.tap_node(sorted(candidates,
                                 key=lambda node: float(node.get('y', 0)))[0])
        else:
            self.device.click(105, 171)
        time.sleep(6)

    def open_video_results(self):
        """当前版无独立视频首页 tab，使用搜索结果的“视频”筛选替代。"""
        self.return_home()
        self.open_search()
        self.search_keyword('图片')
        self.tap('视频', max_y=190, wait=6)

    def open_first_video_result(self):
        images = self._image_nodes(min_y=180)
        if images:
            self.tap_node(images[0])
        else:
            self.device.click(100, 370)
        time.sleep(10)

    def browse_slow(self, up, down, interval=5):
        for start, end, count in ((0.78, 0.24, up), (0.24, 0.78, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(interval)

    def pinch_zoom_in(self):
        window = self.device(type='XCUIElementTypeWindow').get(timeout=5)
        window.pinch(2.0, 1.0)
        time.sleep(2)

    def pinch_zoom_out(self):
        window = self.device(type='XCUIElementTypeWindow').get(timeout=5)
        window.pinch(0.5, -1.0)
        time.sleep(2)

    def repeat_pinch_cycle(self, count):
        for _ in range(count):
            self.pinch_zoom_in()
            self.pinch_zoom_out()
