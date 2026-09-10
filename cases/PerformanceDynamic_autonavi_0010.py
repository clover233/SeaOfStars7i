import time

from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0010(AutonaviCase):
    """Excel 7.0.2：高德地图导航至西安北站。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '点击搜索框，搜索西安北站北进站口')
            self.search('西安北站北进站口')
            self.step(3, '点击路线，点击驾车，点击开始导航')
            self.tap_first_route()
            self.select_driving()
            self.start_navigation()
            self.step(4, '导航界面停留10s')
            time.sleep(10)
            self.step(5, '点击退出，切换到退出导航界面')
            self.open_exit_navigation()
            self.step(6, '点击退出导航，结束导航')
            self.confirm_exit_navigation()
            self.step(7, '返回高德地图主界面')
            self.return_autonavi_home()
            with self.capture_trace(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
