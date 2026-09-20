from aw import SeaOfStarsAW
from cases.meituan_common import MeituanCase


class PerformanceDynamic_meituan_0090(MeituanCase):
    """浏览美团首页及美食团购页面。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动美团')
                self.start_meituan()
            self.step(2, '首页滑动浏览，上滑5次')
            self.browse(5, 0)
            self.step(3, '首页滑动浏览，下滑5次')
            self.browse(0, 5)
            self.step(4, '点击美食团购')
            self.open_food_group_buy()
            self.step(5, '滑动浏览美食团购页面，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(6, '返回美团主界面')
            self.return_meituan_home()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
