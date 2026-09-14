from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_eggparty_0010(WdaCase):
    """Excel 7.0.2：启动蛋仔派对后返回桌面。"""

    PACKAGE = 'com.netease.party'
    APP_NAME = '蛋仔派对'

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动蛋仔派对')
                self.start_app(wait=7)
            with self.capture_trace(iteration, 2):
                self.step(2, '滑动返回Home页')
                self.launcher()
