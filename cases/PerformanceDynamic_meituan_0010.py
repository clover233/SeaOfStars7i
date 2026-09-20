from aw import SeaOfStarsAW
from cases.meituan_common import MeituanCase


class PerformanceDynamic_meituan_0010(MeituanCase):
    """进入外卖并往返浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动美团')
                self.start_meituan()
            self.step(2, '点击外卖')
            self.open_takeout()
            self.step(3, '滑动浏览外卖页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(4, '返回美团主界面')
            self.return_meituan_home()
            with self.capture_trace_5s(iteration, 5):
                self.step(5, '滑动返回Home页')
                self.launcher()
