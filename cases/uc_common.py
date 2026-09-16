"""UC 浏览器动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class UcCase(WdaCase):
    PACKAGE = 'com.ucweb.iphone.lowversion'
    APP_NAME = 'UC浏览器'

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
        """信息流和短视频持续刷新时不等待 XCTest 进入 idle。"""
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
            logging.exception('设置 UC 浏览器连续页面模式失败')

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
            logging.exception('结束 UC 浏览器进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def fail_if_manual_confirmation_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('同意并继续', nodes=nodes) is not None or
                self.find('用户协议和隐私政策', contains=True,
                          nodes=nodes) is not None):
            self.fail('UC浏览器尚未确认隐私协议，请先人工确认后再运行')
        if (self.find('请完成验证', contains=True, nodes=nodes) is not None or
                self.find('拖动滑块', contains=True, nodes=nodes) is not None):
            self.fail('UC浏览器触发安全验证，请先人工完成验证再运行')

    def dismiss_optional_prompts(self):
        """关闭非必要权限、升级提示和新手引导。"""
        for _ in range(6):
            nodes = self.nodes()
            self.fail_if_manual_confirmation_required(nodes)
            button = self.find(
                '不允许', '要求App不跟踪', '要求 App 不跟踪',
                '以后再说', '下次再说', '暂不开启', '暂不更新',
                '我知道了', '取消', '稍后', '跳过', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=180, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def is_home_feed(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.find('推荐', max_y=170, nodes=nodes) is not None and
                self.find('Home', min_y=760, nodes=nodes) is not None)

    def start_uc(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_home_feed(nodes):
                return
            home = self.find('Home', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(5)
                if self.is_home_feed():
                    return
                continue
            back = self.find('back', 'btnTopBarBack', max_y=150, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            elif self.find('说点什么', min_y=740, nodes=nodes) is not None:
                # 新闻正文左上返回箭头为画布元素，2026-09-16 实机
                # 402 x 874 的中心坐标约为 (24, 80)。
                self.device.click(24, 80)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
            time.sleep(4)
        self.fail('多次返回后仍未到达 UC 浏览器主界面')

    def horizontal_browse(self, left, right):
        """在信息流中间左右切频道，避开 iOS 左边缘返回手势。"""
        for _ in range(left):
            self.device.swipe(0.84, 0.48, 0.16, 0.48, 0.3)
            time.sleep(1)
        for _ in range(right):
            self.device.swipe(0.16, 0.48, 0.84, 0.48, 0.3)
            time.sleep(1)
        time.sleep(1)

    def select_channel(self, name):
        self.tap(name, max_y=170, wait=5)

    def open_first_news(self):
        """选择当前推荐流顶部第一条宽卡片，标题每天可以变化。"""
        candidates = []
        excluded = ('NFTableViewCellSparatorLine', '垂直滚动条',
                    '水平滚动条', '关闭信息', '广告')
        for node in self.nodes():
            name = self.node_name(node)
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            height = float(node.get('height', 0))
            if (node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeOther',
                                     'XCUIElementTypeStaticText',
                                     'XCUIElementTypeButton')
                    and 165 <= y <= 730
                    and width >= 250
                    and 18 <= height <= 90
                    and name
                    and not any(word in name for word in excluded)):
                candidates.append(node)
        candidates.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        if candidates:
            self.tap_node(candidates[0])
        else:
            # 2026-09-16 实机 402 x 874；频道栏下第一条标题中心。
            logging.warning('UC新闻卡片未暴露给 WDA，使用实机核对坐标')
            self.device.click(201, 210)
        time.sleep(7)
        deadline = time.monotonic() + 10
        while True:
            nodes = self.nodes()
            if (self.find('back', max_y=150, nodes=nodes) is not None or
                    self.find('Back', min_y=760, nodes=nodes) is not None or
                    self.find('EDVideo', contains=True, nodes=nodes)
                    is not None or
                    self.find('说点什么', min_y=740, nodes=nodes)
                    is not None):
                return
            if time.monotonic() >= deadline:
                self.fail('点击第一条推荐新闻后未进入详情页')
            time.sleep(0.5)

    def open_search(self):
        # 首页搜索框由 UC 自绘，层级仅暴露天气和热词子控件；点击框体中心。
        self.device.click(200, 88)
        time.sleep(4)
        if self.find('urlInputField', max_y=130) is None:
            self.fail('点击首页搜索框后未进入搜索页面')

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        # 当前版本右侧“搜索”按钮的稳定 accessibility name 为
        # btnTopBarCancel，文字 label 才是“搜索”。
        self.tap('btnTopBarCancel', fallback=(346, 84), max_y=130,
                 timeout=8, wait=7)
        nodes = self.nodes()
        self.fail_if_manual_confirmation_required(nodes)
        keyword_marker = self.find(keyword, contains=True, max_y=120,
                                   nodes=nodes)
        back = self.find('Back', min_y=760, nodes=nodes)
        if keyword_marker is None or back is None:
            self.fail('搜索“{}”后未进入搜索结果页'.format(keyword))

    def return_search_page(self):
        self.tap('Back', min_y=760, wait=5)
        if self.find('urlInputField', max_y=130) is None:
            self.fail('从搜索结果返回后未到达搜索发现页面')

    def open_first_search_discovery(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            x = float(node.get('x', 0))
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and name not in ('搜索',)
                    and x < 260 and 110 <= y <= 190 and width >= 80):
                candidates.append(node)
        candidates.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        if candidates:
            self.tap_node(candidates[0])
        else:
            # 搜索发现胶囊由画布绘制时不会出现在 source 中；第一卡位
            # 固定在搜索框下方左侧，内容会随运营配置变化。
            logging.warning('UC搜索发现卡片未暴露给 WDA，使用第一卡位坐标')
            self.device.click(105, 137)
        time.sleep(7)
        nodes = self.nodes()
        if (self.find('Back', min_y=760, nodes=nodes) is None or
                self.find('urlInputField', max_y=130, nodes=nodes) is not None):
            self.fail('点击第一条搜索发现后未进入详情结果页')
