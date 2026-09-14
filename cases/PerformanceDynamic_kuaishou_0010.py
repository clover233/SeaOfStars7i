from aw import SeaOfStarsAW
from cases.kuaishou_common import KuaishouCase


class PerformanceDynamic_kuaishou_0010(KuaishouCase):
    """Excel 7.0.2：精选视频、评论、点赞和收藏。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动快手')
                self.start_app(wait=5)
            self.normalize_featured_after_launch()
            self.step(2, '精选页面上滑切换视频，播放10s，重复3次')
            for _ in range(3):
                self.swipe_to_next_video(watch_seconds=10)
            self.step(3, '点击评论，拉起评论页')
            self.open_comments()
            self.step(4, '评论页上滑2次，下滑2次，返回视频页')
            self.browse_comments_and_close()
            self.step(5, '点击赞')
            self.like_current_video()
            self.step(6, '点击收藏')
            self.collect_current_video()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
