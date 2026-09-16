from aw import SeaOfStarsAW
from cases.ths_common import ThsCase


class PerformanceDynamic_ths_0040(ThsCase):
    """Excel 7.0.2：浏览同花顺自选股票。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动同花顺')
                self.start_ths()
            self.step(2, '点击自选')
            self.open_watchlist()
            self.step(3, '上滑2次浏览自选股票')
            self.browse(2, 0)
            self.step(4, '下滑2次浏览自选股票')
            self.browse(0, 2)
            self.step(5, '返回同花顺主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
