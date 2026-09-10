import time

from aw import SeaOfStarsAW
from cases.camera_common import CameraCase


class PerformanceDynamic_camera_0040(CameraCase):
    """Excel 7.0.2：通过相机 AI 条或 Siri 咨询夕阳拍摄方法。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动相机')
                self.start_camera()
            self.step(2, '点击底部AI条唤起小艺')
            # 原生 iPhone 相机没有 AI 条，下一步会调用 Siri 作为等价替代。
            self.step(3, '点击输入并发送我要拍夕阳应该怎么拍')
            self.invoke_siri_for_camera_advice('我要拍夕阳应该怎么拍')
            self.step(4, '等待10秒后点击X号')
            time.sleep(10)
            self.close_ai_or_siri()
            with self.capture_trace(iteration, 5):
                self.step(5, '滑动返回Home页')
                self.launcher()
