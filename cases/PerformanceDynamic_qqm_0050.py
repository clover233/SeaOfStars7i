from aw import SeaOfStarsAW
from cases.qqmusic_common import QqMusicCase


class PerformanceDynamic_qqm_0050(QqMusicCase):
    """Excel 7.0.2：暂停QQ音乐底部播放器并退出。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            # 该用例依赖已有歌曲正在播放；不能 terminate，否则会破坏预置。
            self.prepare_iteration(terminate=False)
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动QQ音乐')
                self.start_qqmusic()
            self.step(2, 'QQ音乐首页，点击底部暂停按钮')
            self.pause_miniplayer()
            with self.capture_trace_5s(iteration, 3):
                self.step(3, '滑动返回Home页')
                self.launcher()
