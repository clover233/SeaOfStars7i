import time

from aw import SeaOfStarsAW
from cases.doubao_common import DoubaoCase


class PerformanceDynamic_doubao_0020(DoubaoCase):
    """Excel 7.0.2：豆包拍照、选图合成视频并发起通话。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动豆包')
                self.start_doubao()
            self.step(2, '点击拍照，进行拍摄，确认')
            self.take_photo()
            self.step(3, '输入帮我修图')
            self.input_text('帮我修图')
            self.step(4, '点击发送')
            self.send_composer()
            self.step(5, '点击拍照，进行拍摄，确认')
            self.take_photo()
            self.send_composer()
            self.step(6, '点击+号')
            self.tap('更多', wait=2)
            self._allow_expected_permission()
            self.step(7, '选择从相册选择')
            album = self.find('相册', min_y=500)
            if album is not None:
                self.tap_node(album)
                time.sleep(5)
            self.wait_for('所有照片', timeout=15)
            self.step(8, '上滑3次浏览所有图片')
            self.browse(3, 0)
            self.step(9, '下滑3次浏览所有图片')
            self.browse(0, 3)
            self.step(10, '选择2张照片后点完成')
            self.select_two_photos()
            self.step(11, '在输入框输入合成视频')
            self.input_text('合成视频')
            self.step(12, '点击发送')
            self.send_composer(wait=10)
            self.step(13, '点击右上角电话图标')
            self.start_call()
            self.step(14, '在与豆包通话界面停留15s')
            time.sleep(15)
            self.step(15, '退出通话界面')
            self.hang_up()
            with self.capture_trace(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
