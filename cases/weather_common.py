"""Apple 天气动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class WeatherCase(WdaCase):
    PACKAGE = 'com.apple.weather'
    APP_NAME = '天气'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只在首尾步骤采集，并保证采样窗口不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        """天气背景持续动画时不等待 XCTest 进入 idle。"""
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
            logging.exception('设置天气连续页面模式失败')

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
            logging.exception('结束天气进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭定位、通知、恶劣天气提醒和引导弹窗。"""
        for _ in range(6):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '稍后', '暂不', '取消',
                '我知道了', '继续', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def is_city_weather(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.find('list.bullet', min_y=760, nodes=nodes) is not None
                and self.find('map', min_y=760, nodes=nodes) is not None)

    def _city_cards(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        cards = []
        for node in nodes:
            name = self.node_name(node)
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and 110 <= y < 730
                    and width >= 350
                    and ('最高' in name or '最低' in name)):
                cards.append(node)
        return sorted(cards, key=lambda node: float(node.get('y', 0)))

    def return_main(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_city_weather(nodes):
                return
            close = self.find('xmark', max_y=160, nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(4)
                continue
            done = self.find('checkmark', max_y=150, nodes=nodes)
            if done is not None:
                self.tap_node(done)
                time.sleep(3)
                continue
            cards = self._city_cards(nodes)
            if cards:
                self.tap_node(cards[0])
                time.sleep(5)
                continue
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
            time.sleep(3)
        self.fail('多次返回后仍未到达天气主界面')

    def start_weather(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_main()

    def open_city_list(self):
        self.tap('list.bullet', min_y=760, wait=5)
        if self.find('搜索城市或机场', min_y=760) is None:
            self.fail('点击城市列表按钮后未进入位置列表')

    def open_and_dismiss_city_menu(self):
        """打开城市列表的更多菜单，再按用例要求点空白处收起。"""
        self.tap('更多', max_y=150, wait=2)
        if self.find('pencil', max_y=150) is None:
            self.fail('点击“更多”后未显示城市管理菜单')
        # 点菜单外的左侧空白区，只收起菜单，不进入不能打开城市的编辑态。
        self.device.click(24, 210)
        time.sleep(3)
        nodes = self.nodes()
        if self.find('pencil', max_y=150, nodes=nodes) is not None:
            self.fail('单击空白处后城市管理菜单未收起')
        if not self._city_cards(nodes):
            self.fail('收起菜单后未返回城市列表')

    def open_first_managed_city(self):
        cards = self._city_cards()
        if len(cards) < 2:
            self.fail('位置列表少于2座城市，请预先添加至少2座城市')
        self._city_count = len(cards)
        self.tap_node(cards[0])
        time.sleep(6)
        if not self.is_city_weather():
            self.fail('点击城市管理界面的第一个城市后未进入天气主页')

    def switch_cities(self, left=5, right=5, repeats=5):
        """每轮左5次、右5次；不在动画过程中反复拉取 source。"""
        for _ in range(repeats):
            for _ in range(left):
                # 起止点都避开左右边缘，否则右滑会被 iOS 当成返回手势。
                self.device.swipe(0.75, 0.52, 0.25, 0.52, 0.35)
                time.sleep(0.8)
            for _ in range(right):
                self.device.swipe(0.25, 0.52, 0.75, 0.52, 0.35)
                time.sleep(0.8)
            # 城市数少于单向滑动次数时，最后一次右滑会回到位置列表。
            # 继续下一轮前重新打开第一座城市，避免后续在列表上误滑。
            time.sleep(1)
            nodes = self.nodes()
            if not self.is_city_weather(nodes):
                cards = self._city_cards(nodes)
                if not cards:
                    self.fail('切换城市时离开了天气页，且无法回到城市列表')
                self.tap_node(cards[0])
                time.sleep(4)
        time.sleep(4)
        if not self.is_city_weather():
            self.fail('左右切换城市后离开了天气主页')
