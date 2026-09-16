from aw import SeaOfStarsAW
from cases.ths_common import ThsCase


class PerformanceDynamic_ths_0050(ThsCase):
    """Excel 7.0.2：搜索格力电器并管理自选。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动同花顺')
                self.start_ths()
            self.step(2, '点击自选')
            self.open_watchlist()
            self.step(3, '点击搜索按钮')
            self.open_stock_search()
            self.step(4, '输入格力电器')
            self.input_stock_keyword('格力电器')
            self.step(5, '点击格力电器股票')
            self.open_stock_result('格力电器')
            self.step(6, '点击加自选')
            self.add_current_stock()
            self.step(7, '上滑3次浏览格力电器股票')
            self.browse(3, 0)
            self.step(8, '点击删自选')
            self.remove_current_stock()
            self.step(9, '返回同花顺主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
