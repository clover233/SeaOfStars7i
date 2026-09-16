from aw import SeaOfStarsAW
from cases.qqmusic_common import QqMusicCase


class PerformanceDynamic_qqm_0040(QqMusicCase):
    """Excel 7.0.2：浏览QQ音乐首页并播放音乐卡片。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动QQ音乐')
                self.start_qqmusic()
            self.step(2, '浏览首页，上滑2次，下滑2次')
            self.browse_music(2, 2)
            self.step(3, '点击一个音乐卡片进行播放')
            self.play_first_home_card()
            with self.capture_trace_5s(iteration, 4):
                self.step(4, '滑动返回Home页')
                self.launcher()
