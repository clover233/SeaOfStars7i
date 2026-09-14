from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0080(DouyinCase):
    """Excel 7.0.2：浏览团购、美食商家和团购套餐。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动抖音')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击团购，进入团购页面')
            self.open_group_buy()
            self.step(3, '上滑3次，下滑3次，浏览团购页面')
            self.browse(3, 3)
            self.step(4, '点击美食，进入美食页面')
            self.open_food()
            self.step(5, '上滑3次，下滑3次，浏览美食页面')
            self.browse(3, 3)
            self.step(6, '点击美食页面下的第一个商家')
            self.open_first_food_merchant()
            self.step(7, '上滑3次，下滑3次，浏览商家')
            self.browse(3, 3)
            self.step(8, '点击第一个团购套餐')
            self.open_first_group_package()
            self.step(9, '点击购买')
            self.buy_current_group_package()
            self.step(10, '返回抖音主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
