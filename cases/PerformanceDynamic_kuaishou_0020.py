from aw import SeaOfStarsAW
from cases.kuaishou_common import KuaishouCase


class PerformanceDynamic_kuaishou_0020(KuaishouCase):
    """Excel 7.0.2：搜索、直播榜和快手小店。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动快手')
                self.start_app(wait=5)
            self.normalize_featured_after_launch()
            self.step(2, '点击首页右上角搜索图标')
            self.open_search()
            self.step(3, '搜索华为手机')
            self.search('华为手机')
            self.step(4, '上滑3次，下滑3次浏览搜索结果')
            self.browse(up=3, down=3)
            self.step(5, '返回搜索界面')
            self.return_to_search_home()
            self.step(6, '点击直播榜')
            self.open_live_rank()
            self.step(7, '点击排名第一的直播账号，观看直播15s')
            self.watch_live(seconds=15)
            self.step(8, '上滑查看下一个直播，观看直播15s')
            self.switch_to_next_live(seconds=15)
            self.step(9, '返回快手主界面')
            self.exit_live_and_return_featured()
            self.step(10, '点击左上角三横线')
            self.open_sidebar()
            self.step(11, '点击快手小店')
            self.open_shop()
            self.step(12, '上滑3次下滑3次浏览快手小店推荐页面')
            self.browse(up=3, down=3)
            self.step(13, '点击第一个商品')
            self.open_first_shop_product()
            self.step(14, '点击加入购物袋')
            self.open_add_to_bag()
            self.step(15, '返回快手主界面')
            self.return_main_from_shop()
            with self.capture_trace_5s(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
