from aw import SeaOfStarsAW
from cases.jrtt_common import JrttCase


class PerformanceDynamic_jrtt_0020(JrttCase):
    """浏览视频及视频评论。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动今日头条')
                self.start_jrtt()
            self.step(2, '点击视频')
            self.open_video()
            self.step(3, '滑动浏览视频，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(4, '点击评论按钮')
            self.open_video_comments()
            self.step(5, '滑动浏览评论，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(6, '返回今日头条主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
