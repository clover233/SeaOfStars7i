"""微博动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class WeiboCase(WdaCase):
    PACKAGE = 'com.sina.weibo'
    APP_NAME = '微博'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        self._previous_idle_settings = None
        try:
            settings = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': settings.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': settings.get('animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置微博连续页面模式失败')

    def _restore_idle_settings(self):
        settings = getattr(self, '_previous_idle_settings', None)
        if settings is not None:
            try:
                self.device.appium_settings(settings)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束微博进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭不影响主流程的广告、引导和位置提示。"""
        for _ in range(8):
            nodes = self.nodes()
            if self.find('允许访问位置信息', nodes=nodes) is not None:
                button = self.find('继续', nodes=nodes)
                if button is not None:
                    self.tap_node(button)
                    time.sleep(2)
                    try:
                        self.device.alert.dismiss()
                    except Exception:
                        pass
                    time.sleep(2)
                    continue
            button = self.find(
                '关闭', '暂不添加', '以后再说', '暂不开启',
                '我知道了', '跳过', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def _top_back(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return self.find('WBNavigationBarButtonID',
                         'navigationbar back withtext v3', '返回',
                         max_y=140, nodes=nodes)

    def return_weibo_home(self):
        for _ in range(10):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            home = self.find('微博', min_y=780, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                if self.find('WBNewHomeNavTitleButton0', max_y=130) is not None:
                    return
                continue
            if self.find('videoNewComerGuideControllerView', nodes=nodes) is not None:
                self.device.swipe(0.5, 0.72, 0.5, 0.28, 0.4)
                time.sleep(4)
                continue
            if self._top_back(nodes) is not None:
                self.device.click(22, 76)
                time.sleep(3)
                continue
            self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
            time.sleep(3)
        self.fail('多次返回后仍未到达微博首页')

    def start_weibo(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_weibo_home()
        if self.find('登录', '登录/注册', contains=True) is not None:
            self.fail('微博未登录，请先预置已登录账号')

    def tap_bottom_tab(self, name):
        self.tap(name, min_y=780, wait=5)

    def select_home_channel(self, name):
        self.tap(name, max_y=130, wait=4)

    def open_first_live(self):
        avatars = [node for node in self.nodes()
                   if node.tag == 'XCUIElementTypeButton'
                   and self.node_name(node) == 'WBContactAvatarViewIdentifier'
                   and node.get('visible') == 'true'
                   and 100 <= float(node.get('y', 0)) < 190]
        if not avatars:
            self.fail('关注页顶部没有直播博主，请预先关注至少一个当时可直播的账号')
        avatars.sort(key=lambda node: float(node.get('x', 0)))
        self.tap_node(avatars[0])
        time.sleep(7)
        self.dismiss_optional_prompts()
        if self._top_back() is None:
            self.fail('点击第一个直播博主后未进入内容页')

    def return_from_live(self):
        back = self._top_back()
        if back is None:
            self.fail('直播页未找到返回按钮')
        self.tap_node(back)
        time.sleep(5)
        if self.find('关注', max_y=130) is None:
            self.fail('未返回微博关注页')

    def long_press_video_tab(self):
        video = self.find('视频', min_y=780)
        if video is None:
            x, y = 121, 816
        else:
            x = round(float(video.get('x', 0)) + float(video.get('width', 0)) / 2)
            y = round(float(video.get('y', 0)) + float(video.get('height', 0)) / 2)
        self.device.tap_hold(x, y, 2.0)
        time.sleep(4)

    def open_super_topic_after_long_press(self):
        """旧版长按视频会出现超话；新版改用发现搜索等价进入。"""
        super_topic = self.find('超话', contains=True)
        if super_topic is not None:
            self.tap_node(super_topic)
            time.sleep(6)
            return
        self.return_weibo_home()
        self.tap_bottom_tab('发现')
        self.dismiss_optional_prompts()
        self.open_discover_search('超话')

    def browse_super_topic_index(self):
        self.browse(3, 3)

    def open_first_super_topic(self):
        nodes = self.nodes()
        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and float(node.get('y', 0)) >= 190
                      and node.tag in ('XCUIElementTypeCell', 'XCUIElementTypeButton',
                                       'XCUIElementTypeOther')
                      and '超话' in self.node_name(node)]
        if not candidates:
            candidates = [node for node in nodes
                          if node.get('visible') == 'true'
                          and node.tag == 'XCUIElementTypeCell'
                          and float(node.get('y', 0)) >= 190]
        if not candidates:
            self.fail('当前微博版本的超话搜索结果中没有可打开的超话')
        candidates.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(candidates[0])
        time.sleep(6)

    def long_press_super_topic_tab(self):
        self.return_weibo_home()
        self.device.tap_hold(121, 816, 2.0)
        time.sleep(3)

    def open_video_after_long_press(self):
        video = self.find('视频', min_y=780)
        if video is not None:
            self.tap_node(video)
            time.sleep(5)
        if self.find('videoNewComerGuideControllerView') is not None:
            self.device.swipe(0.5, 0.72, 0.5, 0.28, 0.4)
            time.sleep(4)

    def open_more_hot_searches(self):
        self.tap_bottom_tab('发现')
        self.dismiss_optional_prompts()
        self.tap('更多热搜', contains=True, wait=6)

    def open_first_hot_search(self):
        rows = [node for node in self.nodes()
                if node.get('visible') == 'true'
                and node.tag == 'XCUIElementTypeOther'
                and float(node.get('x', -1)) <= 15
                and float(node.get('width', 0)) >= 350
                and 240 <= float(node.get('y', 0)) < 760
                and self.node_name(node).strip()]
        if not rows:
            self.fail('热搜列表中未找到第一条热搜')
        rows.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(rows[0])
        time.sleep(7)

    def open_first_post(self):
        self.tap('正文', min_y=190, wait=7)
        if self.find('评论', min_y=700) is None:
            self.fail('点击第一条博文后未进入正文页')

    def toggle_like(self):
        node = self.find('赞', '已赞', '取消赞', min_y=700, contains=True)
        if node is None:
            self.fail('正文底部未找到赞按钮')
        self.tap_node(node)
        time.sleep(2)

    def comment_without_sending(self, text='评论'):
        self.tap('评论', min_y=700, wait=3)
        self.enter_text(text, clear=True)

    def cancel_comment(self):
        cancel = self.find('取消', max_y=180)
        if cancel is not None:
            self.tap_node(cancel)
        else:
            self.device.swipe(0.5, 0.35, 0.5, 0.8, 0.25)
        time.sleep(4)

    def open_repost(self):
        self.tap('转发', min_y=700, wait=4)

    def cancel_repost(self):
        self.tap('取消', max_y=180, wait=4)

    def _search_input(self):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeTextView',
                                   'XCUIElementTypeTextField',
                                   'XCUIElementTypeSearchField')
                  and float(node.get('y', 0)) < 170]
        if not fields:
            self.fail('搜索页未找到输入框')
        fields.sort(key=lambda node: float(node.get('y', 0)))
        node = fields[0]
        selector = {'type': node.tag, 'visible': True}
        if node.get('name'):
            selector['name'] = node.get('name')
        return self.device(**selector)

    def open_discover_search(self, query):
        field = next((node for node in self.nodes()
                      if node.tag == 'XCUIElementTypeSearchField'
                      and float(node.get('y', 0)) < 130), None)
        if field is not None:
            self.tap_node(field)
            time.sleep(3)
        element = self._search_input()
        element.clear_text()
        element.set_text(query)
        time.sleep(1)
        search = self.find('搜索', max_y=180)
        if search is not None:
            self.tap_node(search)
        else:
            self.device.send_keys('\n')
        time.sleep(7)

    def choose_user_result(self, query):
        self.tap('用户', max_y=260, wait=5)
        nodes = self.nodes()
        matches = [node for node in nodes
                   if node.get('visible') == 'true'
                   and float(node.get('y', 0)) >= 190
                   and query in self.node_name(node)
                   and node.tag in ('XCUIElementTypeCell', 'XCUIElementTypeButton',
                                    'XCUIElementTypeStaticText', 'XCUIElementTypeOther')]
        if not matches:
            matches = [node for node in nodes
                       if node.get('visible') == 'true'
                       and node.tag == 'XCUIElementTypeCell'
                       and float(node.get('y', 0)) >= 190]
        if not matches:
            self.fail('用户搜索结果中未找到“{}”'.format(query))
        matches.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(matches[0])
        time.sleep(7)

    def open_compose(self):
        self.return_weibo_home()
        self.tap('WBComposeMenuItem', max_y=130, wait=3)
        self.tap('写微博', max_y=200, wait=6)
        if self.find('发微博', max_y=130) is None:
            self.fail('点击写微博后未进入编辑页')

    def type_compose_text(self, text):
        self.enter_text(text, clear=True)

    def open_photo_picker(self):
        # 工具栏只暴露为整体图；照片图标是第一项。
        self.device.click(33, 512)
        time.sleep(5)
        try:
            alert_text = self.device.alert.text
        except Exception:
            alert_text = ''
        if '照片图库' in alert_text or '访问你的照片' in alert_text:
            self.fail('请预先在系统设置中授予微博“完全访问照片”权限')

    def select_nine_photos(self):
        photos = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeImage', 'XCUIElementTypeCell')
                  and 100 <= float(node.get('y', 0)) < 780
                  and float(node.get('width', 0)) >= 80
                  and float(node.get('height', 0)) >= 80]
        if len(photos) >= 9:
            photos.sort(key=lambda node: (
                float(node.get('y', 0)), float(node.get('x', 0))))
            for photo in photos[:9]:
                self.tap_node(photo)
                time.sleep(0.6)
        else:
            for y in (190, 320, 450):
                for x in (67, 201, 335):
                    self.device.click(x, y)
                    time.sleep(0.6)
        if self.find('下一步', contains=True) is None:
            self.fail('选择9张图片后未出现“下一步”，请确保相册至少有9张图片')

    def next_photo_step(self):
        self.tap('下一步', contains=True, wait=6)

    def abandon_compose_and_return_home(self):
        for _ in range(6):
            nodes = self.nodes()
            home = self.find('微博', min_y=780, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                return
            discard = self.find('不保存', '放弃', '删除', nodes=nodes)
            if discard is not None:
                self.tap_node(discard)
                time.sleep(4)
                continue
            cancel = self.find('取消', max_y=150, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(3)
                continue
            if self._top_back(nodes) is not None:
                self.device.click(22, 76)
                time.sleep(3)
                continue
            self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
            time.sleep(3)
        self.fail('未能放弃草稿并返回微博主界面')
