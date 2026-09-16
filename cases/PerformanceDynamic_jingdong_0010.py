from aw import SeaOfStarsAW
from cases.jingdong_common import JingdongCase


class PerformanceDynamic_jingdong_0010(JingdongCase):
    """浏览京东首页、手机数码、分类及电脑商品。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动京东')
                self.start_jingdong()
            self.step(2, '首页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击顶部手机数码')
            self.top_entry('手机数码', fallback=(82, 230))
            self.step(4, '手机数码页面浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '点击分类')
            self.open_category()
            self.step(6, '分类页面浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(7, '点击电脑分类')
            self.open_computer_category()
            self.step(8, '电脑页面浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(9, '点击第一类商品进入')
            self.tap_first_category_product()
            self.step(10, '浏览商品页，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(11, '返回京东主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
