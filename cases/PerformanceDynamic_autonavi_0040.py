from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0040(AutonaviCase):
    """Excel 7.0.2：浏览美食搜索结果并进入导航。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '点击美食')
            self.tap('美食', max_y=300, wait=3)
            self.step(4, '上滑3次浏览美食')
            self.browse(3, 0)
            self.step(5, '下滑3次浏览美食')
            self.browse(0, 3)
            self.step(6, '点击第一条搜索结果')
            self.open_first_result()
            self.step(7, '点击路线')
            self.tap('路线', min_y=300, fallback=(0.86, 0.92), wait=4)
            self.step(8, '点击开始导航')
            self.start_navigation()
            self.step(9, '点击退出按钮')
            self.open_exit_navigation()
            self.step(10, '点击退出导航到搜索结果页面')
            self.confirm_exit_navigation()
            self.step(11, '返回高德地图主界面')
            self.return_autonavi_home()
            with self.capture_trace(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
