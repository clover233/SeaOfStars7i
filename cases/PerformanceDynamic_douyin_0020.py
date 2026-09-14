from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0020(DouyinCase):
    """Excel 7.0.2：浏览抖音直播页面、直播间和小黄车。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动抖音')
                self.start_douyin()
            self.step(2, '点击直播栏，进入直播页面')
            self.open_live_page()
            self.step(3, '上滑3次，浏览直播页面')
            self.swipe_up_times(3)
            self.step(4, '点击进入直播间')
            self.enter_live_room()
            self.step(5, '上滑3次，浏览直播间页面')
            self.swipe_up_times(3)
            self.step(6, '点击直播间小黄车，进入小黄车页面')
            self.open_live_cart()
            self.step(7, '小黄车页面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '返回抖音主界面')
            self.return_main()
            with self.capture_trace(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
