from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0070(AutonaviCase):
    """Excel 7.0.2：开始导航后将高德切至后台。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '输入西安北站并搜索')
            self.enter_search_text('西安北站')
            self.step(4, '点击第一个搜索结果的路线')
            self.tap_first_route()
            self.step(5, '点击开始导航')
            self.select_driving()
            self.start_navigation()
            with self.capture_trace(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
