"""腾讯视频动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class TencentVideoCase(WdaCase):
    PACKAGE = 'com.tencent.live4iphone'
    APP_NAME = '腾讯视频'

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
        """播放器持续动画时不等待 XCTest 进入 idle。"""
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
            logging.exception('设置 WDA 连续页面模式失败')

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
            logging.exception('结束腾讯视频进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def fail_if_security_verification(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('身份核实', contains=True, nodes=nodes) is not None and
                self.find('请拖动下方滑块完成拼图', contains=True,
                          nodes=nodes) is not None):
            self.fail('腾讯视频触发滑块验证，请先人工完成验证再运行')

    def fail_if_privacy_confirmation_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('同意并继续', nodes=nodes) is not None or
                self.find('隐私政策', contains=True, nodes=nodes) is not None):
            self.fail('腾讯视频尚未确认隐私协议，请先人工确认后再运行')

    def dismiss_optional_prompts(self):
        """关闭权限、版本更新和普通运营弹窗。"""
        for _ in range(7):
            nodes = self.nodes()
            self.fail_if_privacy_confirmation_required(nodes)
            self.fail_if_security_verification(nodes)
            button = self.find(
                '不允许', '要求App不跟踪', '要求 App 不跟踪',
                '以后再说', '下次再说', '暂不开启', '暂不更新',
                '我知道了', '取消', '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=180, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_tencentvideo(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_main()

    def edge_back(self, wait=3):
        back = self.find('返回', '返回按钮', contains=True, max_y=160)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_main(self):
        for _ in range(10):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            search_box = self.find('搜索框', contains=True, max_y=150,
                                   nodes=nodes)
            home_channel = self.find('首页', max_y=150, nodes=nodes)
            if search_box is not None and home_channel is not None:
                back_to_top = self.find('返回顶部', min_y=760, nodes=nodes)
                if back_to_top is not None:
                    self.tap_node(back_to_top)
                    time.sleep(4)
                return
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                if self.find('搜索框', contains=True, max_y=150) is not None:
                    return
                continue
            if (self.find('金币中心', max_y=200, nodes=nodes) is not None or
                    self.find('更多服务', contains=True, nodes=nodes) is not None):
                # 首页左侧栏打开时没有底栏；点击右侧遮罩关闭侧栏。
                self.device.click(385, 420)
                time.sleep(3)
                continue
            cancel = self.find('取消', max_y=150, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(3)
                continue
            self.edge_back(wait=3)
        self.fail('多次返回后仍未到达腾讯视频主界面')

    def _home_video_candidates(self):
        candidates = []
        for node in self.nodes():
            name = self.node_name(node)
            y = float(node.get('y', 0))
            height = float(node.get('height', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeCell'
                    and name != 'CarouselInnerRoundCell'
                    and '广告' not in name
                    and 'QAD_' not in name
                    and 140 <= y <= 720
                    and height >= 100):
                candidates.append(node)
        return sorted(candidates, key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))

    def open_first_recommended_video(self):
        candidates = self._home_video_candidates()
        if not candidates:
            # 首屏焦点图可能是广告，向上移动一屏后选择第一条普通推荐。
            self.device.swipe(0.5, 0.75, 0.5, 0.42, 0.3)
            time.sleep(3)
            candidates = self._home_video_candidates()
        if candidates:
            self.tap_node(candidates[0])
        else:
            # 2026-09-16 weditor 实测 402 x 874，普通推荐左上卡片
            # 在焦点图下方，滚动后中心约为 (107, 257)。
            logging.warning('推荐视频卡片未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(107, 257)
        time.sleep(5)
        self.dismiss_optional_prompts()
        self._wait_video_content_after_ad()
        started_at = time.monotonic()
        time.sleep(max(0, 30 - (time.monotonic() - started_at)))

    def _video_pixels_ready(self):
        image = self.device.screenshot().convert('L')
        width, height = self.device.window_size()
        if width > height:
            crop = image.crop((0, 0, image.width, image.height))
        else:
            left = round(4 * image.width / width)
            top = round(54 * image.height / height)
            right = round((width - 4) * image.width / width)
            bottom = round(280 * image.height / height)
            crop = image.crop((left, top, right, bottom))
        histogram = crop.histogram()
        total = max(1, sum(histogram))
        non_black = sum(histogram[25:]) / total
        return non_black > 0.08

    def _wait_video_content_after_ad(self, timeout=130):
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            self.fail_if_security_verification(nodes)
            skip = None
            ad_active = False
            for node in nodes:
                if node.get('visible') != 'true':
                    continue
                name = self.node_name(node)
                if ('秒后可跳过广告' in name or
                        name == 'VIP可关闭该广告' or
                        name.startswith('QAD_')):
                    ad_active = True
                if (node.tag == 'XCUIElementTypeButton'
                        and ('跳过广告' in name or name == '跳过')
                        and '秒后' not in name):
                    skip = node
            if skip is not None:
                self.tap_node(skip)
                time.sleep(3)
                continue
            if not ad_active and self._video_pixels_ready():
                return
            if time.monotonic() >= deadline:
                self.fail('等待贴片广告结束或视频画面加载超时')
            time.sleep(2)

    def enter_fullscreen(self):
        self.fail_if_security_verification()
        self.device.click(201, 170)
        time.sleep(1)
        node = self.find('全屏', '横屏', 'fullscreen', 'full screen',
                         contains=True, max_y=330)
        if node is not None:
            self.tap_node(node)
        else:
            # 竖屏播放器的全屏键未稳定暴露；当前 402 x 874 播放器的
            # 右下角位置与旧脚本使用的比例坐标一致。
            self.device.click(378, 250)
        time.sleep(5)
        size = self.device.window_size()
        if size.width <= size.height:
            self.fail('点击全屏按钮后播放器未切换到横屏')

    def exit_fullscreen(self):
        size = self.device.window_size()
        if size.width <= size.height:
            return
        self.device.click(round(size.width / 2), round(size.height / 2))
        time.sleep(1)
        exit_node = self.find(
            '退出全屏', '竖屏', '返回', 'fullscreen', 'full screen',
            contains=True, max_y=180)
        if exit_node is not None:
            self.tap_node(exit_node)
        else:
            # 横屏控制栏不可访问时，标准播放器的退出键位于右下角。
            self.device.click(size.width - 28, size.height - 28)
        time.sleep(5)
        size = self.device.window_size()
        if size.width > size.height:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
            time.sleep(4)
            size = self.device.window_size()
        if size.width > size.height:
            self.fail('退出全屏后仍处于横屏状态')
        if self.find('首页', min_y=760) is not None:
            self.fail('退出全屏时同时离开了视频详情页')

    def open_search(self):
        self.tap('搜索框', contains=True, max_y=150, wait=4)
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeTextField']
        if not fields:
            self.fail('点击搜索框后未进入腾讯视频搜索页')

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        self.device.send_keys('\n')
        time.sleep(7)
        nodes = self.nodes()
        self.fail_if_security_verification(nodes)
        if (self.find('影视', max_y=170, nodes=nodes) is None or
                self.find(keyword, contains=True, min_y=140,
                          nodes=nodes) is None):
            self.fail('搜索“{}”后未进入结果页'.format(keyword))

    def select_video_filter(self):
        self.tap('影视', max_y=170, wait=5)
        if self.find('影视已选中', contains=True, max_y=170) is None:
            self.fail('点击“影视”后筛选状态未切换')
