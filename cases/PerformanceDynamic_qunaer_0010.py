from aw import SeaOfStarsAW
from cases.qunaer_common import QunarCase


class PerformanceDynamic_qunaer_0010(QunarCase):
    """机票、酒店和酒店图片浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动去哪儿旅行')
                self.start_qunar()

            self.step(2, '点击机票，进入机票搜索页面')
            self.open_flight()

            self.step(3, '点击搜索，进入机票搜索结果页面')
            self.search_flight()

            self.step(4, '点击明天')
            self.select_tomorrow()

            self.step(5, '机票搜索结果页上滑5次、下滑5次')
            self.browse(5, 5)

            self.step(6, '上滑到最顶，点击第一个机票方案')
            self.scroll_to_top()
            self.open_first_flight()

            self.step(7, '浏览第一个机票方案，上滑1次、下滑1次')
            self.browse(1, 1)

            self.step(8, '返回去哪儿旅行主界面')
            self.back_tap(count=4)

            self.step(9, '点击酒店，进入酒店页面')
            self.open_hotel()

            self.step(10, '点击城市，选择西安')
            self.choose_xian()

            self.step(11, '点击酒店订单，进入订单页面')
            self.open_hotel_orders()

            self.step(12, '返回酒店界面')
            self.back_tap()

            self.step(13, '点击开始搜索，进入酒店搜索结果页面')
            self.search_hotel()

            self.step(14, '滑动浏览酒店搜索结果，上滑3次、下滑3次')
            self.browse(3, 3)

            self.step(15, '点击第一条搜索结果，进入酒店详情界面')
            self.open_first_hotel()

            self.step(16, '点击酒店图片，查看酒店图片详情')
            self.open_hotel_gallery()

            self.step(17, '图片详情左滑3次、右滑3次')
            self.horizontal_browse(3, 3)

            self.step(18, '返回去哪儿旅行主界面')
            self.back_tap(count=6)

            with self.capture_trace_5s(iteration, 19):
                self.step(19, '滑动返回 Home 页')
                self.launcher()
