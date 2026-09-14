from aw import SeaOfStarsAW
from cases.dianping_common import DianpingCase


class PerformanceDynamic_dazhongdianping_0010(DianpingCase):
    """Excel 7.0.2：搜索烧烤商铺并浏览详情和评价。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动大众点评')
                self.start_dianping()
            self.step(2, '点击美食')
            self.open_food()
            self.step(3, '点击搜索框，输入烧烤')
            self.enter_food_keyword('烧烤')
            self.step(4, '点击搜索')
            self.submit_food_search()
            self.step(5, '滑动浏览烧烤搜索结果，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(6, '点击进入第一家商铺')
            self.open_first_shop()
            self.step(7, '滑动浏览商铺，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '点击评价')
            self.open_reviews()
            self.step(9, '点击查看全部')
            self.open_all_reviews()
            self.step(10, '滑动浏览评论，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(11, '返回美食页面')
            self.return_to_food_page()
            self.step(12, '滑动美食页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(13, '返回大众点评主界面')
            self.return_food_home()
            with self.capture_trace(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
