from aw import SeaOfStarsAW
from cases.momo_common import MomoCase


class PerformanceDynamic_momo_0010(MomoCase):
    """Excel 7.0.2：浏览陌陌首页、直播及各底部页面。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动陌陌')
                self.start_momo()
            self.step(2, '首页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击直播，切换到直播页')
            self.open_tab('直播')
            self.step(4, '直播页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '点击第一个直播观看，等待15秒')
            self.open_first_live()
            self.step(6, '返回直播列表页面')
            self.return_live_list()
            self.step(7, '点击消息tab，切换到消息页')
            self.open_tab('消息')
            self.step(8, '点击小宇宙tab，切换到小宇宙页')
            self.open_tab('小宇宙')
            self.step(9, '点击更多tab，切换到更多页')
            self.open_tab('更多')
            self.step(10, '点击首页，返回陌陌首页')
            self.open_tab('首页')
            with self.capture_trace(iteration, 11):
                self.step(11, '上滑返回Home页')
                self.launcher()
