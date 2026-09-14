import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_hepingjingying_0030(WdaCase):
    """启动和平精英运行30秒后返回Home页。"""

    PACKAGE = 'com.tencent.tmgp.pubgmhd'
    APP_NAME = '和平精英'

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            if self.device.locked():
                self.device.unlock()
                time.sleep(2)
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动和平精英（运行30s）')
                self.start_app(wait=5)
            time.sleep(25)
            with self.capture_trace(iteration, 2):
                self.step(2, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
