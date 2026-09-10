from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0030(AutonaviCase):
    """Excel 7.0.2：浏览西安北站公交地铁路线。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '搜索西安北站')
            self.search('西安北站')
            self.tap_first_route()
            self.step(3, '切换到公交地铁页面')
            self.tap('公共交通', '公交地铁', max_y=220, contains=True, wait=4)
            self.step(4, '上滑1次，下滑1次浏览公交地铁页面')
            self.browse(1, 1)
            self.step(5, '点击第一条路线，上滑1次，下滑1次')
            self.open_first_transit_route()
            self.browse(1, 1)
            self.step(6, '返回高德地图主界面')
            self.return_autonavi_home()
            with self.capture_trace(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
