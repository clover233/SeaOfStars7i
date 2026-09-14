import time

from aw import SeaOfStarsAW
from cases.hongguo_common import HongguoCase


class PerformanceDynamic_hongguomianfeiduanju_0010(HongguoCase):
    """Excel 7.0.2：浏览剧场榜单与观看历史。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动红果免费短剧')
                self.start_hongguo()
            self.step(2, '向上抛滑5次，浏览首页')
            self.swipe_vertical(5, 0)
            self.step(3, '向下抛滑5次，浏览首页')
            self.swipe_vertical(0, 5)
            self.step(4, '点击剧场按钮，进入剧场页面')
            self.open_theatre()
            self.step(5, '向上滑动5次，浏览找剧页面')
            self.swipe_vertical(5, 0)
            self.step(6, '向下滑动5次，浏览找剧页面')
            self.swipe_vertical(0, 5)
            self.step(7, '点击排行榜，进入红果推荐榜')
            self.open_ranking()
            self.step(8, '向上滑动5次，浏览红果推荐榜')
            self.swipe_vertical(5, 0)
            self.step(9, '向下滑动5次，浏览红果推荐榜')
            self.swipe_vertical(0, 5)
            self.step(10, '点击推荐榜第一的短剧，观看视频15s')
            self.open_first_ranking_card()
            time.sleep(15)
            self.step(11, '返回红果推荐榜')
            self.return_from_video()
            self.step(12, '点击热播榜')
            self.tap('热播榜', max_y=300, wait=3)
            self.step(13, '向上滑动5次，浏览热播榜')
            self.swipe_vertical(5, 0)
            self.step(14, '向下滑动5次，浏览热播榜')
            self.swipe_vertical(0, 5)
            self.step(15, '点击热播榜第一的短剧，观看视频15s')
            self.open_first_ranking_card()
            time.sleep(15)
            self.step(16, '返回剧场界面')
            self._edge_back()
            self.return_to_theatre()
            self.step(17, '点击我的，进入我的界面')
            self.open_my()
            self.step(18, '上滑一次，浏览观看历史')
            self.swipe_vertical(1, 0)
            self.step(19, '下滑一次，浏览观看历史')
            self.swipe_vertical(0, 1)
            self.step(20, '点击首页')
            self.tap('首页', min_y=760, wait=3)
            with self.capture_trace(iteration, 21):
                self.step(21, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
