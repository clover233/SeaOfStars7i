"""iOS 设置动态性能用例公共能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class SettingCase(WdaCase):
    PACKAGE = 'com.apple.Preferences'
    APP_NAME = '设置'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
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
            logging.exception('结束设置进程失败，继续启动')
        time.sleep(1)

    def point(self, x_ratio, y_ratio):
        size = self.device.window_size()
        return round(size.width * x_ratio), round(size.height * y_ratio)

    def click_ratio(self, x_ratio, y_ratio, wait=2):
        self.device.click(*self.point(x_ratio, y_ratio))
        time.sleep(wait)

    def return_to_root(self, count=7):
        # iOS 设置会恢复上次子页；连续点导航栏返回位，抵达首页后为空白区。
        for _ in range(count):
            # y=0.114 同时命中普通返回按钮和“添加新墙纸”的 xmark。
            self.click_ratio(0.065, 0.114, wait=0.6)
        time.sleep(2)

    def start_settings(self, root=True):
        self.start_app(wait=4)
        if root:
            self.return_to_root()

    def open_apple_account(self):
        # 登录和未登录状态标题不同，优先使用系统稳定 identifier。
        self.tap_scrolling('com.apple.settings.primaryAppleAccount',
                           'Apple账户', wait=4)

    def close_apple_account(self):
        # 未登录设备的 Apple 账户页是模态框，右上角为关闭按钮而非返回。
        self.click_ratio(0.905, 0.114, wait=3)

    def drag_brightness(self):
        sliders = [node for node in self.nodes()
                   if node.tag == 'XCUIElementTypeSlider'
                   and node.get('visible') == 'true']
        if not sliders:
            self.fail('显示与亮度页未找到亮度滑块')
        slider = sliders[0]
        x = float(slider.get('x', 0))
        y = float(slider.get('y', 0))
        width = float(slider.get('width', 0))
        height = float(slider.get('height', 0))
        center_y = round(y + height / 2)
        self.device.swipe(round(x + width * 0.35), center_y,
                          round(x + width * 0.75), center_y, 0.8)
        time.sleep(1)
        self.device.swipe(round(x + width * 0.75), center_y,
                          round(x + width * 0.35), center_y, 0.8)
        time.sleep(2)

    def tap_scrolling(self, *names, wait=3, contains=False, attempts=6):
        """在设置列表中查找入口；不可见时双向滚动后再点击。"""
        for direction in ('up', 'down'):
            for _ in range(attempts):
                node = self.find(*names, contains=contains)
                if node is not None:
                    self.tap_node(node)
                    time.sleep(wait)
                    return
                if direction == 'up':
                    self.device.swipe(0.5, 0.78, 0.5, 0.26, 0.35)
                else:
                    self.device.swipe(0.5, 0.26, 0.5, 0.78, 0.35)
                time.sleep(0.6)
        self.fail('未找到设置入口：{}'.format(' / '.join(names)))

    def open_wallpaper_settings(self):
        self.tap_scrolling('墙纸', 'Wallpaper', wait=4)

    def open_new_wallpaper(self):
        # add-new-button 是横向墙纸卡片的容器，真正可进入图库的是下方按钮。
        self.tap_scrolling('add-new-wallpaper-button',
                           '添加新墙纸', 'Add New Wallpaper',
                           wait=5, contains=True)

    def open_wallpaper_gallery(self):
        self.open_wallpaper_settings()
        self.open_new_wallpaper()

    def browse_wallpaper_candidates(self, up=1, down=1):
        self.browse(up, down)

    def home_page_browse(self, left=3, right=3):
        for start, end, count in ((0.88, 0.12, left), (0.12, 0.88, right)):
            for _ in range(count):
                self.device.swipe(start, 0.50, end, 0.50, 0.35)
                time.sleep(0.7)
