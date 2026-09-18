from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0060(WeixinCase):
    """Excel 7.0.2：朋友圈拍摄、相册预览与位置。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '进入朋友圈')
            self.tap('发现', min_y=760, wait=2)
            self.tap('朋友圈', min_y=80, max_y=220, wait=4)
            self.step(3, '点击右上角相机')
            self.open_moments_camera_menu()
            self.step(4, '点击拍摄')
            self.tap('拍摄', min_y=600, wait=3)
            self.step(5, '关闭相机，返回朋友圈')
            self.tap('关闭', max_y=140, wait=3)
            self.step(6, '再次点击右上角相机')
            self.open_moments_camera_menu()
            self.step(7, '从手机相册选择图片3张')
            self.tap('从手机相册选择', min_y=650, wait=4)
            self.select_photos(3)
            self.step(8, '点击预览')
            self.tap('预览(3)', contains=True, min_y=740, wait=3)
            self.step(9, '左滑2次浏览图片')
            self.horizontal_browse(0, 2)
            self.step(10, '点击右上角完成')
            self.tap('完成', contains=True, min_y=740, wait=4)
            self.step(11, '点击所在位置')
            self.tap('所在位置', min_y=350, max_y=650, wait=4)
            self.step(12, '选择第一个具体位置并完成')
            self.choose_first_moment_location()
            self.step(13, '取消发表（替代已失效的左滑返回）')
            self.tap('取消', max_y=120, wait=2)
            self.step(14, '点击不保留')
            self.tap('不保留', min_y=500, wait=3)
            self.step(15, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
