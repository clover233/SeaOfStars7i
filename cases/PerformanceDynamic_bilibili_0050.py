import time

from aw import SeaOfStarsAW
from cases.bilibili_common import BilibiliCase


class PerformanceDynamic_bilibili_0050(BilibiliCase):
    """Excel 7.0.2：浏览直播页和直播间，并横屏观看直播。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动哔哩哔哩')
                self.start_bilibili()
            self.step(2, '点击直播，进入直播页面')
            self.open_channel('直播')
            self.step(3, '上滑5次、下滑5次浏览直播页')
            self.browse(5, 5)
            self.step(4, '点击第一个直播，进入直播间')
            self.open_first_live()
            self.step(5, '上滑5次、下滑5次浏览直播间')
            self.browse(5, 5)
            self.step(6, '观看直播10秒')
            time.sleep(10)
            self.step(7, '切换至横屏观看直播20秒')
            self.enter_live_landscape()
            time.sleep(20)
            self.step(8, '返回首页')
            self.return_bilibili_home()
            with self.capture_trace(iteration, 9):
                self.step(9, '上滑返回桌面')
                self.launcher()
