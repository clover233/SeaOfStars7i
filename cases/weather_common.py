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

    def enter_manage_cities(self):
        self.tap('更多', max_y=150, wait=2)
        # 当前系统只暴露菜单图标名；pencil 对应可见文字“编辑列表”。
        self.tap('pencil', max_y=150, wait=4)
        if self.find('checkmark', max_y=150) is None:
            self.fail('点击“编辑列表”后未进入城市管理状态')

    def open_first_managed_city(self):
        # iOS 26 编辑状态下城市卡片不可打开，先完成编辑再选第一项。
        done = self.find('checkmark', max_y=150)
        if done is not None:
            self.tap_node(done)
            time.sleep(4)
        cards = self._city_cards()
        if len(cards) < 2:
            self.fail('位置列表少于2座城市，请预先添加至少2座城市')
        self.tap_node(cards[0])
        time.sleep(6)
        if not self.is_city_weather():
            self.fail('点击城市管理界面的第一个城市后未进入天气主页')

    def switch_cities(self, left=5, right=5, repeats=5):
        """按 Excel 原文执行5轮，每轮左5次、右5次。"""
        for _ in range(repeats):
            for _ in range(left):
                self.device.swipe(0.84, 0.42, 0.16, 0.42, 0.25)
                time.sleep(0.6)
            for _ in range(right):
                self.device.swipe(0.16, 0.42, 0.84, 0.42, 0.25)
                time.sleep(0.6)
        time.sleep(2)
        if not self.is_city_weather():
            self.fail('左右切换城市后离开了天气主页')

    def open_more_weather(self):
        """用当前版本的10日预报详情替代已移除的“查看更多天气”。"""
        for _ in range(8):
            nodes = self.nodes()
            daily_rows = []
            for node in nodes:
                name = self.node_name(node)
                y = float(node.get('y', 0))
                width = float(node.get('width', 0))
                if (node.get('visible') == 'true'
                        and node.tag == 'XCUIElementTypeButton'
                        and 100 <= y < 780
                        and width >= 350
                        and '°' in name
                        and '最高' not in name
                        and '最低' not in name):
                    daily_rows.append(node)
            if daily_rows:
                daily_rows.sort(key=lambda node: float(node.get('y', 0)))
                self.tap_node(daily_rows[0])
                time.sleep(6)
                break
            self.device.swipe(0.5, 0.76, 0.5, 0.32, 0.3)
            time.sleep(1)
        else:
            self.fail('未找到10日天气预报入口')
        nodes = self.nodes()
        if (self.find('天气状况', max_y=180, nodes=nodes) is None or
                self.find('xmark', max_y=180, nodes=nodes) is None):
            self.fail('点击近日天气后未进入天气状况详情')

    def browse_recent_weather(self):
        self.device.swipe(0.84, 0.4, 0.16, 0.4, 0.3)
        time.sleep(2)
        self.device.swipe(0.16, 0.4, 0.84, 0.4, 0.3)
        time.sleep(2)
        if self.find('天气状况', max_y=180) is None:
            self.fail('左右查看近日天气时离开了天气状况详情')

    def close_weather_detail(self):
        self.tap('xmark', max_y=180, wait=5)
        if not self.is_city_weather():
            self.fail('关闭天气状况详情后未返回天气主界面')

