from aw import SeaOfStarsAW
from cases.cloudmusic_common import CloudMusicCase


class PerformanceDynamic_cloudmusic_0010(CloudMusicCase):
    """Excel 7.0.2：网易云音乐浏览并播放推荐歌单。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动网易云音乐')
                self.start_cloudmusic()
            self.step(2, '首页浏览，上滑2次，下滑2次，重复2次')
            self.browse_home()
            self.step(3, '点击雷达歌单下的第一个歌单')
            self.open_first_playlist()
            self.step(4, '播放全部')
            self.play_all()
            self.step(5, '点击下一首，重复5次')
            self.next_tracks(5)
            self.step(6, '暂停播放')
            self.pause_playback()
            with self.capture_trace(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
