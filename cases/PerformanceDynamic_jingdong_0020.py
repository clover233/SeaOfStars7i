from aw import SeaOfStarsAW
from cases.jingdong_common import JingdongCase


class PerformanceDynamic_jingdong_0020(JingdongCase):
    """京东超市购物及秒送外卖链路。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动京东')
                self.start_jingdong()
            self.step(2, '点击京东超市')
            self.open_supermarket()
            self.step(3, '点击粮油调味')
            self.open_grocery()
            self.step(4, '粮油调味页面浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '加入第一个商品到购物车')
            self.add_first_grocery_item()
            self.step(6, '点击结算')
            self.checkout_visible_cart()
            self.step(7, '点击新建地址')
            self.tap('新建地址', '新增收货地址', contains=True,
                     fallback=(238, 154), wait=4)
            self.step(8, '返回京东主界面')
            self.return_home()
            self.step(9, '点击购物车')
            self.bottom_tab('购物车')
            self.step(10, '点击去结算')
            self.checkout_visible_cart()
            self.step(11, '返回京东主界面')
            self.return_home()
            self.step(12, '点击秒送')
            self.open_seconds()
            self.step(13, '秒送界面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(14, '点击外卖')
            self.open_takeout()
            self.step(15, '外卖页面上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(16, '点击第一个外卖商家')
            self.open_first_merchant()
            self.step(17, '商家页面上滑1次，下滑1次')
            self.browse(1, 1)
            self.step(18, '点击第一个商品加入购物车')
            self.add_first_merchant_item()
            self.step(19, '返回商铺并点击购物车图标')
            self.open_merchant_cart()
            self.step(20, '点击结算')
            self.checkout_merchant()
            self.step(21, '返回购物车并清空商品')
            self.edge_back()
            self.tap('清空', '删除', contains=True, fallback=(365, 115), wait=3)
            self.step(22, '返回京东主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 23):
                self.step(23, '滑动返回Home页')
                self.launcher()
