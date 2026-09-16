from aw import SeaOfStarsAW
from cases.sodamusic_common import SodaMusicCase


class PerformanceDynamic_sodamusic_0010(SodaMusicCase):
    """Excel 7.0.2：汽水音乐搜索、播放和歌单浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动汽水音乐')
                self.start_sodamusic()
            self.step(2, '点击右上角搜索')
            self.open_search()
            self.step(3, '搜索国歌')
            self.search('国歌')
            self.step(4, '上滑2次，下滑2次浏览国歌')
            self.browse(2, 2)
            self.step(5, '返回首页')
            self.return_home()
            self.step(6, '点击下方播放按钮，播放15S后暂停')
            self.play_for_15_seconds_and_pause()
            self.step(7, '点击右下角我的')
            self.open_mine()
            self.step(8, '点击我喜欢的音乐')
            self.open_liked_music()
            self.step(9, '返回首页')
            self.return_home()
            self.step(10, '点击右下角省略号打开播放列表')
            self.open_playlist()
            self.step(11, '返回汽水音乐主界面')
            self.close_playlist()
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
