import logging
import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_meituxiuxiu_0010(WdaCase):
    """Excel 7.0.2：导入图片、拍照并分别完成调色保存。"""

    PACKAGE = 'com.meitu.mtxx'
    APP_NAME = '美图秀秀'

    def dismiss_startup_popups(self):
        # 相册权限是导入图片的必要预置；通知等权限不属于本用例。
        if self.device(label='允许完全访问').exists:
            self.device(label='允许完全访问').click()
            time.sleep(3)
        if self.find('VIP热门功能', contains=True) is not None:
            logging.info('关闭美图秀秀 VIP 推荐弹框')
            self.device.click(0.81, 0.20)
            time.sleep(2)

    def dismiss_camera_permission(self):
        nodes = self.nodes()
        alert_text = ' '.join(self.node_name(node) for node in nodes)
        allow = self.find('允许', nodes=nodes)
        if allow is not None and ('相机' in alert_text or '摄像头' in alert_text):
            self.tap_node(allow)
            time.sleep(3)

    def return_to_home(self):
        for _ in range(4):
            nodes = self.nodes()
            if (self.find('图片美化', nodes=nodes) is not None
                    and self.find('相机', nodes=nodes) is not None):
                return
            home = self.find('icon publish home', nodes=nodes)
            if home is not None:
                self.tap_node(home)
            else:
                self.device.click(0.05, 0.085)
            time.sleep(2)
        self.fail('未能返回美图秀秀主界面')

    def choose_first_photo(self):
        nodes = self.nodes()
        if self.find('图片', nodes=nodes) is None:
            self.fail('未进入图片选择页；请确认相册中至少有一张图片')
        # 图片缩略图由自绘网格呈现，WDA 树中没有可点击的 Cell。
        self.device.click(0.12, 0.21)
        time.sleep(6)
        if self.find('滤镜') is None:
            self.fail('第一张图片未能进入编辑页')

    def confirm_editor_panel(self):
        # 编辑页右下角确认图标没有 accessibility name。
        self.device.click(0.945, 0.947)
        time.sleep(3)

    def collapse_camera_filter(self):
        self.device.click(0.925, 0.936)
        time.sleep(2)
        shutter = self.find('videoModeView')
        if shutter is None or float(shutter.get('width', 0)) < 60:
            self.fail('滤镜弹框未成功收起')

    def set_brightness_to_100(self):
        self.tap('调色', wait=2)
        self.tap('亮度', wait=1)
        # 亮度滑杆的最右端，对应 100%。
        self.device.click(0.84, 0.782)
        time.sleep(1)
        self.confirm_editor_panel()

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动美图秀秀')
                self.start_app(wait=5)
            self.dismiss_startup_popups()
            self.return_to_home()

            self.step(2, '点击导入图片，切换到图片页面')
            self.tap('图片美化', '导入图片', wait=4)
            self.dismiss_startup_popups()

            self.step(3, '选择第一张图片，点击滤镜')
            self.choose_first_photo()
            self.tap('滤镜', wait=2)

            self.step(4, '选中从左往右第一种滤镜格式，并确认')
            self.tap('旷野', fallback=(0.25, 0.89), wait=1)
            self.confirm_editor_panel()

            self.step(5, '点击调色，并设置亮度为100%，点击确认')
            self.set_brightness_to_100()

            self.step(6, '点击保存')
            self.tap('保存', wait=7)

            self.step(7, '点击再修一张，切换到图片页面')
            self.tap('再修一张', wait=4)

            self.step(8, '返回美图秀秀主界面')
            self.return_to_home()

            self.step(9, '点击相机')
            self.tap('相机', wait=5)
            self.dismiss_camera_permission()

            self.step(10, '点击滤镜')
            self.tap('滤镜调色', '滤镜', wait=3)

            self.step(11, '切换一次滤镜')
            self.tap('硬汉', fallback=(0.25, 0.88), wait=2)

            self.step(12, '点击右下角箭头收起滤镜弹框')
            self.collapse_camera_filter()

            self.step(13, '点击快门进行拍照')
            shutter = self.find('videoModeView')
            if shutter is not None:
                self.tap_node(shutter)
            else:
                self.device.click(0.5, 0.87)
            time.sleep(6)

            self.step(14, '点击编辑')
            self.tap('去修图', '编辑', wait=6)

            self.step(15, '点击调色，并设置亮度为100%，点击确认')
            self.set_brightness_to_100()

            self.step(16, '点击保存')
            self.tap('保存', wait=7)

            self.step(17, '点击再修一张，切换到图片页面')
            self.tap('再修一张', wait=4)

            self.step(18, '返回美图秀秀主界面')
            self.return_to_home()

            with self.capture_trace(iteration, 19):
                self.step(19, '滑动返回Home页')
                self.launcher()
