from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0090(DouyinCase):
    """Excel 7.0.2：进入直播间并浏览小黄车。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动抖音')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击直播栏，进入直播页面')
            self.open_live_page()
            self.step(3, '点击第一个进入直播间')
            self.enter_live_room()
            self.step(4, '点击小黄车，进入小黄车页面')
            self.open_live_cart()
            self.step(5, '小黄车页面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(6, '返回抖音主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
