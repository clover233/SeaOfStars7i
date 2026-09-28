"""快手动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class KuaishouCase(WdaCase):
    PACKAGE = 'com.jiangjia.gif'
    APP_NAME = '快手'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾维测打点至少覆盖 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                remaining = 5 - (time.monotonic() - started_at)
                if remaining > 0:
                    time.sleep(remaining)

    def _enable_continuous_ui_mode(self):
        """视频和直播持续刷新时不要等待 XCTest 进入 idle。"""
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
                'accessibilityDeadline': current.get('accessibilityDeadline', 0),
            }
            self.device.appium_settings({
                'waitForIdleTimeout': 0,
                'animationCoolOffTimeout': 0,
                'accessibilityDeadline': 5,
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
        self._screen_size = self.device.window_size()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束快手进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 12)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def _is_featured_feed(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return self.find('kFeatureCoverViewAccessId', nodes=nodes) is not None

    def _featured_controls_ready(self, nodes):
        return (self._is_featured_feed(nodes)
                and self.find('home_bottom_tab_id_thanos', nodes=nodes) is not None
                and self.find('分享至', '分享给朋友', contains=True,
                              nodes=nodes) is None)

    def normalize_featured_after_launch(self):
        """关闭启动弹窗并进入精选视频流。"""
        self.return_featured()

    def return_featured(self):
        for _ in range(10):
            nodes = self.nodes()
            if self._featured_controls_ready(nodes):
                return
            share_title = self.find('分享给朋友', '分享至', nodes=nodes)
            if share_title is not None:
                # 长按菜单的“关闭”是弹幕选项；点击标题上方的遮罩收起。
                size = self.device.window_size()
                self.device.click(round(size.width / 2),
                                  round(max(140, float(share_title.get('y', 0)) - 50)))
                time.sleep(2)
                continue
            panel_close = self.find('default panel close compact',
                                    '取消', '关闭', nodes=nodes)
            if panel_close is not None:
                self.tap_node(panel_close)
                time.sleep(2)
                continue
            back = self.find(
                'common nav back black', 'user_profile_go_back_button',
                nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(5, 430, 360, 430, 0.3)
            time.sleep(4)
        self.fail('多次返回后仍未到达快手精选页面')

    def swipe_to_next_video(self, watch_seconds=10):
        self.return_featured()
        self.device.swipe(0.5, 0.75, 0.5, 0.25, 0.3)
        time.sleep(watch_seconds)
        # 动画结束时第一份 source 偶尔还未暴露底栏；返回检查会等待
        # 控件稳定。该检查成功后即已回到精选页，不再无条件报失败。
        self.return_featured()

    def open_comments(self):
        self.tap('COMMENT', wait=4)
        self.wait_for('关闭评论区', timeout=10)

    def browse_comments_and_close(self):
        self.browse(up=2, down=2)
        close = self.find('关闭评论区')
        if close is not None:
            self.tap_node(close)
            time.sleep(4)
        # 评论面板到顶后下拉也可能直接关闭，先确认视频页再继续。
        self.return_featured()
        self.wait_for('COMMENT', timeout=10)

    def like_current_video(self):
        self.tap('LIKE', wait=3)

    def collect_current_video(self):
        self.tap('COLLECT', wait=3)

    def open_search(self):
        nodes = self.nodes()
        search = self.find('搜索', max_y=130, nodes=nodes)
        if search is None:
            search = self.find(
                'feed navigationbars search 40 ', max_y=130, nodes=nodes)
        if search is None:
            self.fail('精选页面未找到右上角搜索入口')
        self.tap_node(search)
        time.sleep(4)
        self.wait_for('search_home_input', timeout=10)

    def search(self, keyword):
        self.tap('search_home_input', max_y=130, wait=1)
        self.enter_text(keyword)
        nodes = self.nodes()
        buttons = [node for node in self.matching_nodes('搜索', nodes=nodes)
                   if node.tag == 'XCUIElementTypeButton']
        if not buttons:
            self.fail('搜索页未找到“搜索”按钮')
        self.tap_node(buttons[0])
        time.sleep(6)
        self.wait_for('search_result_input', timeout=15)

    def return_to_search_home(self):
        self.tap('common nav back black', max_y=130, wait=5)
        self.wait_for('直播榜', timeout=12)

    def open_live_rank(self):
        self.tap('直播榜', wait=5)
        # 榜单卡片由画布渲染，WDA 树仍停留在搜索页。第一名坐标由
        # 402x874 设备上的 WEditor 核对，并以是否进入直播画布校验。
        self.device.click(160, 510)
        time.sleep(7)
        nodes = self.nodes()
        if (self.find('search_home_input', nodes=nodes) is not None
                or self.find('common nav back black', nodes=nodes) is not None):
            self.fail('点击直播榜第一名后未进入直播间')

    def watch_live(self, seconds=15):
        time.sleep(seconds)

    def switch_to_next_live(self, seconds=15):
        self.device.swipe(0.5, 0.75, 0.5, 0.25, 0.3)
        time.sleep(seconds)

    def exit_live_and_return_featured(self):
        size = self._screen_size
        # 430x932 实机：旧 (371,70) 点到了观众头像；退出 X 在屏幕最右侧。
        nodes = self.nodes()
        if self.find('观众榜单前10可获得专属勋章', nodes=nodes) is not None:
            self.device.click(round(size.width * 0.5), round(size.height * 0.3))
            time.sleep(2)
        self.device.click(round(size.width * 0.948), round(size.height * 0.079))
        time.sleep(4)
        nodes = self.nodes()
        if self.find('看了这么久，留个关注再走吧！', nodes=nodes) is not None:
            exit_button = self.find('退出直播间', '退出', nodes=nodes)
            if exit_button is not None:
                self.tap_node(exit_button)
            else:
                self.device.click(round(size.width * 200 / 402),
                                  round(size.height * 525 / 874))
            time.sleep(4)
        self.return_featured()

    def open_sidebar(self):
        self.tap('侧边栏', max_y=130, wait=4)
        self.wait_for('快手小店', timeout=10)

    def open_shop(self):
        self.tap('快手小店', wait=8)
        nodes = self.nodes()
        if self.find('kwaishop-pub-dapaidabu-h5', nodes=nodes) is not None:
            # 2026-09-28：大牌大补为从底部弹出的活动页，点击上方遮罩关闭。
            size = self._screen_size
            self.device.click(round(size.width * 0.5), round(size.height * 0.16))
            time.sleep(3)
        self.wait_for('我的订单', timeout=15)

    def open_first_shop_product(self):
        size = self.device.window_size()
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true' and len(name) >= 12
                    and 0 <= x <= size.width * 0.1
                    and size.height * 0.29 <= y <= size.height * 0.83
                    and size.width * 0.35 <= width <= size.width * 0.5
                    and 12 <= height <= 60):
                candidates.append(node)
        if not candidates:
            self.fail('快手小店推荐页未找到第一个商品')
        self.tap_node(sorted(candidates, key=lambda node: float(
            node.get('y', 0)))[0])
        # 商品已打开时新版返回按钮可能无名称，以底部交易入口判断详情页。
        self.wait_for('立即购买', '加入购物车', '加入购物袋',
                      min_y=size.height * 0.75, contains=True, timeout=15)

    def open_add_to_bag(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeImage'
                    and ('cartIcon_' in name or (
                        130 <= x <= 180 and 780 <= y <= 840
                        and 20 <= width <= 45 and 20 <= height <= 45))):
                candidates.append(node)
        if candidates:
            self.tap_node(candidates[0])
        else:
            logging.warning('加入购物袋未暴露节点，使用 weditor 核对坐标')
            size = self.device.window_size()
            self.device.click(round(size.width * 160 / 402),
                              round(size.height * 818 / 874))
        time.sleep(5)
        self.wait_for('加入购物车', '请选择规格', contains=True, timeout=12)

    def return_main_from_shop(self):
        nodes = self.nodes()
        if self.find('请选择规格', nodes=nodes) is not None:
            # 关闭规格面板，不执行购买或提交订单。
            self.device.click(375, 195)
            time.sleep(3)

        for _ in range(6):
            nodes = self.nodes()
            if self._is_featured_feed(nodes):
                return
            back = self.find('merchant_transaction_back_transparent', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                # 小店 Web 页面左上角返回箭头未暴露名称。
                self.device.click(20, 83)
            time.sleep(5)
        self.fail('多次返回后仍未到达快手主界面')
