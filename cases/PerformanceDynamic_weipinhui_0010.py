from aw import SeaOfStarsAW
from cases.weipinhui_common import WeipinhuiCase


class PerformanceDynamic_weipinhui_0010(WeipinhuiCase):
    """唯品会搜索、商品、店铺、购物车与结算浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动唯品会')
                self.start_weipinhui()
            self.step(2, '搜索清风卫生纸')
            self.search_product('清风卫生纸')
            self.step(3, '浏览搜索结果，上滑2次、下滑3次')
            self.browse(2, 3)
            self.step(4, '点击第一条商品查看详情')
            self.open_first_product()
            self.step(5, '浏览商品详情，上滑2次、下滑3次')
            self.browse(2, 3)
            self.step(6, '进入店铺浏览，上滑3次、下滑3次')
            self.open_store()
            self.browse(3, 3)
            self.step(7, '返回商品详情')
            self.return_product_detail()
            self.step(8, '加入购物车')
            self.add_to_cart()
            self.step(9, '点击购物车')
            self.open_cart()
            self.step(10, '点击结算')
            self.open_checkout()
            self.step(11, '返回购物车界面')
            self.return_to_cart()
            self.step(12, '长按商品')
            self.long_press_top_cart_item()
            self.step(13, '点击删除')
            self.delete_revealed_cart_item()
            self.step(14, '返回唯品会主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
