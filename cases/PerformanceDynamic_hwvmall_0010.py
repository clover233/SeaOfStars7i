from aw import SeaOfStarsAW
from cases.hwvmall_common import HuaweiMallCase


class PerformanceDynamic_hwvmall_0010(HuaweiMallCase):
    """Excel 7.0.2：轮播图、搜索和商品详情浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动华为商城')
                self.start_app(wait=5)
            self.normalize_home_after_launch()

            self.step(2, '点击第一个轮播图，进入轮播图详情页')
            self.open_current_carousel()
            self.step(3, '浏览轮播图详情页，上滑3次，下滑3次')
            self.browse(up=3, down=3)
            self.return_home()

            self.step(4, '点击第二个轮播图，进入轮播图详情页')
            self.advance_carousel()
            self.open_current_carousel()
            self.step(5, '浏览轮播图详情页，上滑3次，下滑3次')
            self.browse(up=3, down=3)
            self.return_home()

            self.step(6, '点击第三个轮播图，进入轮播图详情页')
            self.advance_carousel()
            self.open_current_carousel()
            self.step(7, '浏览轮播图详情页，上滑3次，下滑3次')
            self.browse(up=3, down=3)
            self.return_home()

            self.step(8, '点击搜索框，搜索p60')
            self.open_search()
            self.search('p60')
            self.step(9, '浏览搜索结果上滑5次，下滑5次')
            self.browse(up=5, down=5)
            self.step(10, '查看商品详情，点击进入商品详情页')
            self.open_first_search_product()
            # 工作簿将下一行也编号为 10；按实际顺序记为步骤 11。
            self.step(11, '浏览商品详情上滑6次，下滑6次')
            self.browse(up=6, down=6)
            self.step(12, '返回华为商城主界面')
            self.return_home()
            self.step(13, '华为商城首页上滑6次，下滑6次')
            self.browse(up=6, down=6)
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
