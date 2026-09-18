from aw import SeaOfStarsAW
from cases.xianyu_common import XianyuCase


class PerformanceDynamic_xianyu_0010(XianyuCase):
    """Excel 7.0.2：闲鱼搜索和分享商品。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动闲鱼')
                self.start_xianyu()
            self.finish_xianyu_start()
            self.step(2, '首页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(3, '点击搜索框，进入搜索页')
            self.open_search()
            self.step(4, '搜索华为mate60')
            self.search('华为mate60')
            self.step(5, '搜索结果上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(6, '点击第一个商品，进入商品详情页')
            self.open_first_product()
            self.step(7, '商品详情页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(8, '点击分享，等待4秒后返回')
            self.open_and_close_share()
            self.step(9, '返回闲鱼主界面')
            self.return_xianyu_home()
            with self.capture_trace_5s(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
