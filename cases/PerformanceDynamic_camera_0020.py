from aw import SeaOfStarsAW
from cases.camera_common import CameraCase


class PerformanceDynamic_camera_0020(CameraCase):
    """Excel 7.0.2：按多个焦段拍照并浏览相机控制和图库。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动相机')
                self.start_camera()
            self.step(2, '点击广角W，点击拍照')
            self.set_wide_zoom()
            self.capture_photo()
            self.step(3, '点击1X，点击拍照')
            self.set_one_x()
            self.capture_photo()
            self.step(4, '点击2X，点击拍照')
            self.set_two_x()
            self.capture_photo()
            self.step(5, '点击10X，点击拍照（如果现在iPhone没有，调到最高倍）')
            self.set_max_zoom()
            self.capture_photo()
            self.step(6, '底部点击箭头拉起设置页面')
            self.open_controls()
            self.step(7, '点击设置')
            self.open_settings_or_skip()
            self.step(8, '设置页面上滑1次，下滑1次，重复3次')
            self.browse_settings_or_controls()
            self.step(9, '点击照片比例')
            self.open_aspect_ratio()
            self.step(10, '点击取消，关闭照片比例弹框')
            self.close_aspect_ratio()
            self.step(11, '点击照片格式')
            self.skip_unsupported('照片格式弹框')
            self.step(12, '点击取消，关闭照片格式弹框')
            self.skip_unsupported('照片格式弹框的取消按钮')
            self.step(13, '点击声控拍照')
            self.skip_unsupported('声控拍照')
            self.step(14, '点击取消，关闭声控拍照弹框')
            self.skip_unsupported('声控拍照弹框的取消按钮')
            self.step(15, '侧滑返回预览框')
            self.close_controls()
            self.step(16, '点击小艺视觉（如果没有跳过）')
            self.try_xiaoyi_vision()
            self.step(17, '点击拍照')
            self.capture_photo()
            self.step(18, '侧滑返回扫一扫页面')
            self.skip_unsupported('小艺视觉扫一扫页面')
            self.step(19, '点击左侧图库图标拉起图库（如果没有跳过）')
            self.open_photo_library()
            self.step(20, '图库上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(21, '侧滑返回扫一扫页面')
            self.return_from_photo_library()
            self.step(22, '返回相机主界面')
            self.ensure_photo_mode()
            with self.capture_trace(iteration, 23):
                self.step(23, '滑动返回Home页')
                self.launcher()
