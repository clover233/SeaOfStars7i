from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0010(DouyinCase):
    """Excel 7.0.2：浏览抖音推荐视频并发表评论。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动抖音')
                self.start_douyin()
            self.step(2, '浏览推荐视频3次')
            self.swipe_up_times(3)
            self.step(3, '点击评论按钮，浏览评论并上滑1次')
            self.open_comments()
            self.browse_comments_once(close_after=True)
            self.step(4, '浏览推荐视频3次')
            self.swipe_up_times(3)
            self.step(5, '点击评论按钮，浏览评论并上滑1次')
            self.open_comments()
            self.browse_comments_once(close_after=False)
            self.step(6, '点击输入框')
            self.focus_comment_input()
            self.step(7, '输入我是评论ABC')
            self.enter_comment('我是评论ABC')
            self.step(8, '点击发送')
            self.send_comment()
            self.step(9, '返回抖音主界面')
            self.return_main()
            with self.capture_trace(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
