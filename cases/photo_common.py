"""iOS Photos dynamic-performance case helpers."""

import logging
import re
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class PhotoCase(WdaCase):
    PACKAGE = 'com.apple.mobileslideshow'
    APP_NAME = '照片'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """Capture only the requested step and keep each trace at least 5 seconds."""
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
            logging.exception('结束照片进程失败，继续启动')
        time.sleep(1)

    def dismiss_optional_prompts(self):
        for _ in range(5):
            button = self.find('继续', '开始使用照片', '以后再说',
                               '暂不开启', '我知道了')
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def start_photos(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        if self.find('LibraryTab', 'CollectionsTab') is None:
            self.fail('照片应用首页未加载')

    def tap_identifier(self, identifier, *labels, wait=2, timeout=6):
        return self.tap(identifier, *labels, wait=wait, timeout=timeout)

    def open_library(self, wait=3):
        self.tap_identifier('LibraryTab', '图库', wait=wait)

    def open_collections(self, wait=3):
        self.tap_identifier('CollectionsTab', '精选集', wait=wait)

    def _pinch(self, scale, velocity, count=1):
        window = self.device(type='XCUIElementTypeWindow')
        for _ in range(count):
            window.pinch(scale, velocity)
            time.sleep(0.8)

    def normalize_day_view(self):
        # iOS 26 Photos has no Year/Month/Day buttons. The closest day view is
        # the largest library zoom level.
        self._pinch(2.0, 1.0, count=3)

    def cycle_library_scale(self, count=1):
        for _ in range(count):
            self._pinch(0.5, -1.0, count=2)
            self._pinch(2.0, 1.0, count=2)

    def fling_library(self, up, down):
        for start, end, count in ((0.82, 0.20, up), (0.20, 0.82, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.10)
                time.sleep(0.6)

    def drag_library(self, up, down):
        for start, end, count in ((0.78, 0.28, up), (0.28, 0.78, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 1.0)
                time.sleep(0.4)

    def drag_library_scrollbar(self, up, down):
        size = self.device.window_size()
        x = round(size.width * 0.95)
        top = round(size.height * 0.26)
        bottom = round(size.height * 0.76)
        for start, end, count in ((bottom, top, up), (top, bottom, down)):
            for _ in range(count):
                self.device.swipe(x, start, x, end, 0.8)
                time.sleep(0.4)

    def ensure_minimum_photos(self, minimum=6):
        for node in self.nodes():
            text = node.get('label') or node.get('value') or ''
            match = re.fullmatch(r'(\d+)张照片', text)
            if match:
                if int(match.group(1)) < minimum:
                    self.fail('至少需要{}张照片，当前只有{}张'.format(
                        minimum, match.group(1)))
                return
        logging.warning('未读取到图库照片数，将在打开首张照片时校验')

    def open_first_library_photo(self):
        size = self.device.window_size()
        # Photo tiles in the iOS 26 library are canvas-rendered and absent from
        # WDA's accessibility tree. This coordinate was verified on the current
        # 402x874 device and is expressed proportionally for other screen sizes.
        self.device.click(round(size.width * 0.50), round(size.height * 0.40))
        time.sleep(3)
        if self.find('PUOneUpBarButtonItemIdentifierDone') is None:
            # Dense-grid fallback: select the first visible tile.
            self.device.click(round(size.width * 0.10), round(size.height * 0.20))
            time.sleep(3)
        if self.find('PUOneUpBarButtonItemIdentifierDone') is None:
            self.fail('未打开照片大图；请至少预置1张照片')

    def swipe_preview_strip(self, direction, count):
        strip = self.find('照片选取器')
        if strip is None:
            self.fail('大图页未显示底部照片预览条')
        x, y, width, height = (float(strip.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        center_y = round(y + height / 2)
        self.device.click(round(x + width / 2), center_y)
        time.sleep(0.5)
        left = round(x + width * 0.18)
        right = round(x + width * 0.82)
        start, end = (left, right) if direction == 'right' else (right, left)
        for _ in range(count):
            self.device.swipe(start, center_y, end, center_y, 0.35)
            time.sleep(0.6)

    def leave_one_up(self):
        self.tap_identifier('PUOneUpBarButtonItemIdentifierDone', '返回', wait=2)

    def edge_back_from_one_up(self):
        # On iOS Photos this gesture normally changes assets instead of popping
        # the viewer. Perform the requested gesture, then use the real Back item
        # when the viewer remains open.
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(1)
        if self.find('PUOneUpBarButtonItemIdentifierDone') is not None:
            logging.warning('大图页侧滑被 iOS 解释为切换照片，改用“返回”退出')
            self.leave_one_up()

    def _scroll_until(self, predicate, direction='up', attempts=8):
        for _ in range(attempts):
            node = predicate(self.nodes())
            if node is not None:
                return node
            if direction == 'up':
                self.device.swipe(0.5, 0.75, 0.5, 0.25, 0.35)
            else:
                self.device.swipe(0.5, 0.25, 0.5, 0.75, 0.35)
            time.sleep(0.6)
        return None

    def open_albums_page(self):
        # Photos restores the last nested Collections page after relaunch. If
        # that page is already Albums, tapping the selected Collections tab is
        # a no-op and the shelf entry is no longer present to search for.
        if self.find('AlbumsBarCreateMenu') is not None:
            return
        self.open_collections()

        def album_heading(nodes):
            matches = [node for node in nodes
                       if node.get('visible') == 'true'
                       and node.get('name') == 'albums-shelf-details-disclosure'
                       and float(node.get('x', 0)) < 100]
            return matches[0] if matches else None

        node = self._scroll_until(album_heading, direction='down')
        if node is None:
            node = self._scroll_until(album_heading, direction='up')
        if node is None:
            self.fail('精选集页未找到“相簿”入口')
        self.tap_node(node)
        time.sleep(3)
        if self.find('AlbumsBarCreateMenu') is None:
            self.fail('未进入相簿页')

    @staticmethod
    def _album_count(node):
        label = node.get('label') or ''
        match = re.search(r'相簿，(\d+)个(?:资源|项目)', label)
        return int(match.group(1)) if match else None

    def first_nonempty_album(self):
        def candidate(nodes):
            albums = [node for node in nodes
                      if node.tag == 'XCUIElementTypeButton'
                      and node.get('visible') == 'true'
                      and node.get('name') == 'album'
                      and (self._album_count(node) or 0) > 0]
            return albums[0] if albums else None

        node = self._scroll_until(candidate, direction='up')
        if node is None:
            self.fail('没有可浏览的非空相簿；请至少预置1个含照片的相簿')
        return node

    def open_album_node(self, node):
        label = node.get('label') or ''
        self.tap_node(node)
        time.sleep(3)
        if self.find('PXBarItemIdentifierExplicitBack') is None:
            self.fail('未打开相簿：{}'.format(label or '未知相簿'))
        return label

    def find_album(self, label):
        def candidate(nodes):
            for node in nodes:
                if (node.tag == 'XCUIElementTypeButton'
                        and node.get('visible') == 'true'
                        and node.get('name') == 'album'
                        and node.get('label') == label):
                    return node
            return None

        node = self._scroll_until(candidate, direction='up', attempts=5)
        if node is None:
            node = self._scroll_until(candidate, direction='down', attempts=5)
        return node

    def back_to_albums(self):
        # A long downward drag at the top of an iOS 26 album can dismiss the
        # album page and leave us here already. Treat that as a successful
        # return instead of requiring a now-absent Back item.
        if self.find('AlbumsBarCreateMenu') is not None:
            return
        self.tap_identifier('PXBarItemIdentifierExplicitBack', '返回', wait=3)
        if self.find('AlbumsBarCreateMenu') is None:
            self.fail('未返回相簿页')

    def edge_back_from_album(self):
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(2)
        if self.find('PXBarItemIdentifierExplicitBack') is not None:
            logging.warning('相簿页侧滑未返回，改用导航栏“返回”')
            self.back_to_albums()

    def open_media_types_page(self):
        if self.find('AlbumsBarCreateMenu') is not None:
            self.tap_identifier('BackButton', '精选集', wait=3)
        self.open_collections()

        def heading(nodes):
            matches = [node for node in nodes
                       if node.get('visible') == 'true'
                       and node.get('name') == 'media-types-shelf-details-disclosure'
                       and float(node.get('x', 0)) < 100]
            return matches[0] if matches else None

        node = self._scroll_until(heading, direction='up')
        if node is None:
            self.fail('精选集页未找到“媒体类型”入口')
        self.tap_node(node)
        time.sleep(3)
        if self.find('MediaTypesBarEditButton') is None:
            self.fail('未进入媒体类型页')

    def open_videos(self):
        for node in self.nodes():
            label = node.get('label') or ''
            if (node.tag == 'XCUIElementTypeButton'
                    and node.get('visible') == 'true'
                    and node.get('name') == 'media-type'
                    and label.startswith('视频，')):
                self.tap_node(node)
                time.sleep(3)
                return
        self.fail('没有可删除的测试视频；请预置1段视频并确保首个视频可删除')

    def open_first_album_asset(self, expected='asset'):
        layout = self.find('photos_sectioned_layout')
        if layout is None:
            self.fail('当前页面没有可打开的媒体网格')
        x, y, width, height = (float(layout.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        visible_top = max(y, 150)
        visible_bottom = min(y + height, 780)
        if visible_bottom <= visible_top:
            self.fail('媒体网格不在可见区域')
        self.device.click(round(x + width / 6),
                          round((visible_top + visible_bottom) / 2))
        time.sleep(3)
        if self.find('PUOneUpBarButtonItemIdentifierDone') is None:
            self.fail('未打开第一个{}'.format(
                '视频' if expected == 'video' else '文件'))

    def delete_open_video(self):
        trash = self.find('PUOneUpBarButtonItemIdentifierTrashBin')
        if trash is None:
            size = self.device.window_size()
            self.device.click(round(size.width / 2), round(size.height / 2))
            time.sleep(0.5)
            trash = self.find('PUOneUpBarButtonItemIdentifierTrashBin')
        if trash is None:
            self.fail('视频大图页未找到删除按钮')
        self.tap_node(trash)
        time.sleep(1)
        confirm = self.find('删除视频', '删除')
        if confirm is None:
            self.fail('删除视频确认框未出现')
        self.tap_node(confirm)
        time.sleep(3)

    def return_from_videos_to_albums(self):
        # When more videos remain, Photos advances to the next video's one-up
        # view after deletion. Reveal its hidden controls and leave that view
        # before using the Collections tab.
        if self.find('OneUpMainPagingView') is not None:
            done = self.find('PUOneUpBarButtonItemIdentifierDone')
            if done is None:
                size = self.device.window_size()
                self.device.click(round(size.width / 2), round(size.height / 2))
                time.sleep(0.5)
                done = self.find('PUOneUpBarButtonItemIdentifierDone')
            if done is None:
                self.fail('删除视频后无法退出大图页')
            self.tap_node(done)
            time.sleep(2)
        # The Videos collection replaces the global tab bar with its own
        # toolbar. Pop Videos -> Media Types -> Collections before navigating
        # to Albums.
        if self.find('PXBarItemIdentifierExplicitBack') is not None:
            self.tap_identifier('PXBarItemIdentifierExplicitBack', '返回', wait=2)
        if self.find('MediaTypesBarEditButton') is not None:
            self.tap_identifier('BackButton', '精选集', wait=2)
        self.open_albums_page()

    def ensure_album_absent(self, album_name):
        for node in self.nodes():
            label = node.get('label') or ''
            if (node.tag == 'XCUIElementTypeButton'
                    and node.get('name') == 'album'
                    and label.startswith(album_name + '相簿，')):
                self.fail('已存在同名相簿“{}”；请先删除或改名，避免误删'.format(
                    album_name))

    def open_new_album_form(self):
        self.tap_identifier('AlbumsBarCreateMenu', '添加', wait=1)
        self.tap_identifier('rectangle.stack.badge.plus', '新建相簿', wait=2)
        if self.find('LemonadeCollectionCustomizationTitleField') is None:
            self.fail('新建相簿页未打开')

    def create_album(self, album_name):
        field = self.device(name='LemonadeCollectionCustomizationTitleField')
        field.clear_text()
        field.set_text(album_name)
        time.sleep(1)
        self.tap_identifier(
            'LemonadeCollectionCustomizationNavigationViewCreateButton',
            '创建', wait=4)
        if self.find('AlbumsBarCreateMenu') is None:
            self.fail('创建相簿后未返回相簿页')

    def open_named_album(self, album_name):
        prefix = album_name + '相簿，'

        def candidate(nodes):
            for node in nodes:
                if (node.tag == 'XCUIElementTypeButton'
                        and node.get('visible') == 'true'
                        and node.get('name') == 'album'
                        and (node.get('label') or '').startswith(prefix)):
                    return node
            return None

        node = self._scroll_until(candidate, direction='down', attempts=5)
        if node is None:
            self.fail('未找到新建相簿“{}”'.format(album_name))
        return self.open_album_node(node)

    def open_album_picker(self):
        self.tap_identifier('PhotosGridAddButton', '添加照片', wait=4)
        if self.find('Cancel') is None:
            self.fail('相簿文件选择器未打开')

    def tap_picker_segment(self, label):
        self.return_to_picker_root()
        candidates = [node for node in self.nodes()
                      if node.tag == 'XCUIElementTypeButton'
                      and node.get('visible') == 'true'
                      and (node.get('label') == label or node.get('name') == label)
                      and float(node.get('y', 0)) < 150]
        if not candidates:
            self.fail('文件选择器未找到“{}”分页'.format(label))
        self.tap_node(candidates[0])
        time.sleep(2)

    def return_to_picker_root(self):
        # A short WDA swipe in the Collections page can occasionally be
        # interpreted by Photos as opening the collection under the finger.
        # Nested picker pages use BackButton, while the picker root exposes
        # Cancel plus the Photos/Collections segmented control.
        for _ in range(4):
            nodes = self.nodes()
            has_cancel = any(node.get('visible') == 'true'
                             and node.get('name') == 'Cancel'
                             for node in nodes)
            has_segments = all(any(
                node.tag == 'XCUIElementTypeButton'
                and node.get('visible') == 'true'
                and (node.get('name') == label
                     or node.get('label') == label)
                and float(node.get('y', 0)) < 150
                for node in nodes) for label in ('照片', '精选集'))
            if has_cancel and has_segments:
                return
            back = next((node for node in nodes
                         if node.tag == 'XCUIElementTypeButton'
                         and node.get('visible') == 'true'
                         and node.get('name') == 'BackButton'), None)
            if back is None:
                self.fail('无法返回文件选择器的照片/精选集根页面')
            self.tap_node(back)
            time.sleep(2)
        self.fail('文件选择器嵌套层级过深，无法返回根页面')

    def browse_picker(self):
        for label in ('照片', '精选集'):
            self.tap_picker_segment(label)
            self.browse(5, 5)
            self.return_to_picker_root()
        # Leave the picker in the Photos tab so the next test step can select
        # an asset without depending on the final Collections scroll state.
        self.tap_picker_segment('照片')

    def select_first_picker_asset_and_cancel(self):
        self.return_to_picker_root()
        self.tap_picker_segment('照片')
        size = self.device.window_size()
        # Picker asset cells are also canvas-rendered on iOS 26.
        self.device.click(round(size.width / 6), round(size.height * 0.25))
        time.sleep(1)
        self.tap_identifier('Cancel', '取消', wait=3)

    def delete_named_album(self, album_name):
        self.back_to_albums()
        prefix = album_name + '相簿，'

        def candidate(nodes):
            for node in nodes:
                if (node.tag == 'XCUIElementTypeButton'
                        and node.get('visible') == 'true'
                        and node.get('name') == 'album'
                        and (node.get('label') or '').startswith(prefix)):
                    return node
            return None

        node = self._scroll_until(candidate, direction='down', attempts=5)
        if node is None:
            self.fail('未找到待删除的相簿“{}”'.format(album_name))
        x, y, width, height = (float(node.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        self.device.tap_hold(round(x + width / 2), round(y + height / 2), 1.5)
        time.sleep(2)
        self.tap_identifier('trash', '删除相簿', wait=1)
        self.tap_identifier('删除相簿', wait=3)

    def return_to_library_main(self):
        self.open_library(wait=3)
