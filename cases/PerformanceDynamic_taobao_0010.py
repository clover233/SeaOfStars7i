from aw import SeaOfStarsAW
from cases.taobao_common import TaobaoCase


class PerformanceDynamic_taobao_0010(TaobaoCase):
    """Excel 7.0.2：淘宝搜索、评价、客服、店铺和加购。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动淘宝')
                self.start_taobao()
            self.step(2, '点击搜索框，输入并搜索清风卫生纸')
            self.open_search()
            self.search('清风卫生纸')
            self.step(3, '浏览搜索结果，上滑5次，下滑6次')
            self.browse(5, 6)
            self.step(4, '按销量筛选，点击第一条商品查看详情')
            self.sort_by_sales()
            self.open_first_product()
            self.step(5, '浏览商品详情，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(6, '点击查看更多查看宝贝评价')
            self.open_reviews()
            self.step(7, '上滑5次，下滑5次浏览评价页面')
            self.browse(5, 5)
            self.step(8, '返回商品详情')
            self.return_product_detail()
            self.step(9, '点击屏幕底部客服')
            self.open_customer_service()
            self.step(10, '点击输入框发送文字你好')
            self.send_text_message('你好')
            self.step(11, '点击加号相册，选择图片并发送')
            self.send_first_photo()
            self.step(12, '返回商品详情')
            self.return_product_detail()
            self.step(13, '进入店铺并浏览，上滑3次，下滑3次')
            self.enter_store()
            self.browse_store()
            self.step(14, '返回商品详情')
            self.return_product_detail()
            self.step(15, '加入购物车')
            self.add_to_cart()
            self.step(16, '返回淘宝主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 17):
                self.step(17, '滑动返回Home页')
                self.launcher()
