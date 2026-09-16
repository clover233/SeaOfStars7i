from aw import SeaOfStarsAW
from cases.tielu12306_common import Tielu12306Case


class PerformanceDynamic_tielu12306_0020(Tielu12306Case):
    """Excel 7.0.2：铁路12306酒店、订单和会员浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动铁路12306')
                self.start_tielu12306()
            self.step(2, '上滑2次，浏览首页')
            self.browse(2, 0)
            self.step(3, '点击酒店住宿，进入酒店住宿页面')
            self.open_hotel()
            self.step(4, '返回铁路12306主界面')
            self.return_from_hotel()
            self.step(5, '点击出行服务，进入出行服务页面')
            self.open_main_tab('出行服务')
            self.step(6, '点击订单，进入订单页面')
            self.open_main_tab('订单')
            self.step(7, '点击铁路会员，进入会员页面')
            self.open_main_tab('铁路会员')
            self.step(8, '点击首页，进入首页')
            self.open_main_tab('首页')
            self.step(9, '下滑2次，浏览首页')
            self.browse(0, 2)
            with self.capture_trace_5s(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
