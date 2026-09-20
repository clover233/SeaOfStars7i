from aw import SeaOfStarsAW
from cases.meituan_common import MeituanCase


class PerformanceDynamic_meituan_0080(MeituanCase):
    """进入美食团购并上下浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动美团')
                self.start_meituan()
            self.step(2, '点击美食团购')
            self.open_food_group_buy()
            self.step(3, '上滑5次浏览美食团购页面')
            self.browse(5, 0)
            self.step(4, '下滑5次浏览美食团购页面')
            self.browse(0, 5)
            self.step(5, '返回美团主界面')
            self.return_meituan_home()
            with self.capture_trace_5s(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
