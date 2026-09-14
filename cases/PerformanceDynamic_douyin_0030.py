from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0030(DouyinCase):
    """Excel 7.0.2：浏览抖音商城、商品、购物车和团购。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动抖音')
                self.start_douyin()
            self.step(2, '点击商城，切换至商城页面')
            self.open_mall()
            self.step(3, '上滑3次浏览推荐商品')
            self.swipe_up_times(3)
            self.step(4, '下滑3次浏览推荐商品')
            self.swipe_down_times(3)
            self.step(5, '搜索华为p70')
            self.search_mall_product('华为p70')
            self.step(6, '上滑3次浏览搜索结果')
            self.swipe_up_times(3)
            self.step(7, '下滑3次浏览搜索结果')
            self.swipe_down_times(3)
            self.step(8, '点进第一个商品，进入详情页')
            self.open_first_mall_product()
            self.step(9, '点击加入购物车')
            self.add_current_product_to_cart()
            self.step(10, '上滑3次浏览购物车界面')
            self.swipe_up_times(3)
            self.step(11, '点击左下角客服，进入客服页面')
            self.open_customer_service()
            self.step(12, '返回商品详情界面')
            self.return_product_detail()
            self.step(13, '点击左下角进店，查看店铺详情')
            self.enter_store()
            self.step(14, '上滑3次浏览店铺界面')
            self.swipe_up_times(3)
            self.step(15, '返回抖音主界面')
            self.return_mall_home()
            self.step(16, '点击抖音商城首页右上角购物车图标')
            self.open_mall_cart()
            self.step(17, '点击管理按钮')
            self.manage_cart()
            self.step(18, '点击删除')
            self.delete_selected_cart_items()
            self.step(19, '返回抖音商城界面')
            self.return_from_cart()
            self.step(20, '点击团购，进入抖音团购界面')
            self.open_group_buy()
            self.step(21, '上滑3次，下滑3次浏览抖音团购界面')
            self.browse(3, 3)
            with self.capture_trace(iteration, 22):
                self.step(22, '滑动返回Home页')
                self.launcher()
