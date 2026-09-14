import time

from aw import SeaOfStarsAW
from cases.hwvmall_common import HuaweiMallCase


class PerformanceDynamic_hwvmall_0020(HuaweiMallCase):
    """Excel 7.0.2：分类、商品详情、评价和客服。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动华为商城')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击分类')
            self.open_category()
            self.step(3, '上滑5次，下滑5次浏览分类')
            self.browse(up=5, down=5)
            self.step(4, '查看商品详情，返回分类，点击进入商品详情页')
            self.open_first_category_product()
            self.return_to_category()
            self.open_first_category_product()
            self.step(5, '查看商品详情')
            time.sleep(3)
            self.step(6, '上滑5次，下滑5次浏览商品详情')
            self.browse(up=5, down=5)
            self.step(7, '商品详情上滑1次')
            self.swipe_up_once()
            self.step(8, '点击评价')
            self.show_review_section()
            self.step(9, '查看宝贝评价，查看全部')
            self.open_all_reviews()
            self.step(10, '上滑5次，下滑5次浏览评价')
            self.browse(up=5, down=5)
            self.step(11, '返回商品详情')
            self.return_to_product()
            self.step(12, '点击客服')
            self.open_customer_service()
            self.step(13, '返回商品详情')
            self.return_from_customer_service()
            self.step(14, '返回华为商城主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
