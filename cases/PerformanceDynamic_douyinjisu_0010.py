from aw import SeaOfStarsAW
from cases.douyinjisu_common import DouyinJisuCase


class PerformanceDynamic_douyinjisu_0010(DouyinJisuCase):
    """Excel 7.0.2：抖音极速版推荐、视频、作者主页与评论浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动抖音极速版')
                self.start_douyin()
            self.step(2, '点击推荐')
            self.open_recommend()
            self.step(3, '上下滑动5次浏览推荐页')
            self.browse_recommend()
            self.step(4, '点击热点')
            self.open_hotspot()
            self.step(5, '点击第一个视频播放')
            self.play_first_video()
            self.step(6, '点击视频的UP主')
            self.open_author()
            self.step(7, '上下滑动5次浏览UP主主页')
            self.browse_author()
            self.step(8, '点击UP主第一个视频播放')
            self.open_first_author_video()
            self.step(9, '点击查看视频下的评论')
            self.open_comments()
            self.step(10, '返回抖音极速版主界面')
            self.return_main()
            with self.capture_trace(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
