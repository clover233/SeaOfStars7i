import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_happyanimal_0010(WdaCase):
    """启动开心消消乐运行30秒后返回Home页。"""

    PACKAGE = 'com.happyelements.1OSAnimal'
    APP_NAME = '开心消消乐'

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            if self.device.locked():
                self.device.unlock()
                time.sleep(2)
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动开心消消乐（运行30s）')
                self.start_app(wait=5)
            time.sleep(25)
            with self.capture_trace(iteration, 2):
                self.step(2, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
