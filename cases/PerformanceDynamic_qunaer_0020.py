from aw import SeaOfStarsAW
from cases.qunaer_common import QunarCase


class PerformanceDynamic_qunaer_0020(QunarCase):
    """机票预订页、值机选座页和火车车次浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动去哪儿旅行')
                self.start_qunar()

            self.step(2, '点击机票，切换到机票页')
            self.open_flight()

            self.step(3, '点击搜索，查看搜索结果')
            self.search_flight()

            self.step(4, '点击搜索结果第一条查看详情')
            self.open_first_flight()

            self.step(5, '点击预订，切换到订票页面')
            self.open_first_booking()

            self.step(6, '滑动浏览订票页面，上滑2次、下滑2次')
            self.browse(2, 2)

            self.step(7, '侧滑3次返回机票页')
            self.edge_back(count=3)

            self.step(8, '点击值机选座，切换到选座页')
            self.open_checkin_seat()

            self.step(9, '值机选座页上滑1次、下滑1次')
            self.browse(1, 1)

            self.step(10, '侧滑返回去哪儿旅行主页')
            self.edge_back()
            self.back_tap(count=2)

            self.step(11, '点击火车高铁，进入搜索页面')
            self.open_train()
            self.set_train_arrival_from_hot_city()

            self.step(12, '点击搜索，进入车次选择页面')
            self.search_train()

            self.step(13, '返回去哪儿旅行主界面')
            self.back_tap(count=3)

            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回 Home 页')
                self.launcher()
