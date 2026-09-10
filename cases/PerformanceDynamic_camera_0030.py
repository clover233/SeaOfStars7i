import time

from aw import SeaOfStarsAW
from cases.camera_common import CameraCase


class PerformanceDynamic_camera_0030(CameraCase):
    """Excel 7.0.2：拍照、切换摄像头并录制视频。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动相机')
                self.start_camera()
            self.step(2, '点击设置4X对焦（如果现在iPhone没有，调到最高倍）')
            self.set_max_zoom()
            self.step(3, '点击屏幕中间，拍摄一张照片，拍照5次')
            self.capture_photo(count=5, focus=True)
            self.step(4, '点击左下角缩略图查看图片')
            self.open_recent_media()
            self.step(5, '左滑8次查看其它照片')
            self.swipe_media_left(8)
            self.step(6, '返回相机拍照界面')
            self.return_from_recent_media()
            self.step(7, '后置切换前置')
            self.flip_camera()
            self.step(8, '前置切换后置')
            self.flip_camera()
            self.step(9, '点击录像切换到录像模式')
            self.ensure_video_mode()
            self.step(10, '录像设置为4X变焦（如果现在iPhone没有，调到最高倍）、1080p60fps录像模式')
            self.set_max_zoom()
            self.set_video_format(60)
            self.step(11, '开始录像')
            self.tap('VideoCapture', wait=1)
            self.step(12, '录制10S后结束录像')
            time.sleep(10)
            self.tap('VideoCapture', wait=2)
            self.step(13, '录像模式恢复1X变焦，1080p30fps录像模式')
            self.set_one_x()
            self.set_video_format(30)
            self.step(14, '点击左下角查看视频')
            self.open_recent_media()
            self.step(15, '点击播放视频')
            self.play_recent_video()
            self.step(16, '返回相机录像界面')
            self.return_from_recent_media()
            self.step(17, '右滑进入拍照界面')
            self.return_to_photo_by_swipe()
            with self.capture_trace(iteration, 18):
                self.step(18, '滑动返回Home页')
                self.launcher()
