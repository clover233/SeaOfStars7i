from aw import SeaOfStarsAW
from cases.bilibili_common import BilibiliCase


class PerformanceDynamic_bilibili_0020(BilibiliCase):
    """Excel 7.0.2：浏览推荐视频、UP 主主页和评论。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动哔哩哔哩')
                self.start_bilibili()
            self.step(2, '点击推荐')
            self.open_channel('推荐')
            self.step(3, '浏览推荐，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(4, '点击热门')
            self.open_channel('热门')
            self.step(5, '点击的第一个视频播放')
            self.open_first_hot_video()
            self.step(6, '点击视频的up主')
            self.open_up_profile()
            self.step(7, '浏览up主，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '点击up主第一个视频播放')
            self.open_first_profile_video()
            self.step(9, '点击视频下的评论')
            self.open_comments()
            self.step(10, '浏览评论，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(11, '返回哔哩哔哩主界面')
            self.return_bilibili_home()
            with self.capture_trace(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
