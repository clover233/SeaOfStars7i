from aw import SeaOfStarsAW
from cases.xhs_common import XhsCase


class PerformanceDynamic_xhs_0020(XhsCase):
    """小红书首页、收藏视频和评论浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动小红书')
                self.start_xhs()

            self.step(2, '首页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(3, '打开一条首页内容，上下各滑动5次后返回')
            self.open_first_feed_note()
            self.browse(5, 5)
            self.edge_back()
            self.step(4, '点击我，进入个人页面')
            self.open_profile()
            self.step(5, '点击收藏，进入收藏页面')
            self.open_collection()
            self.step(6, '打开一条已收藏的视频')
            self.open_collected_video()
            self.step(7, '点击左下角点赞')
            self.toggle_like()
            self.step(8, '点击评论，进入评论页面')
            self.open_comments()
            self.step(9, '评论页面上滑3次、下滑3次')
            self.browse(3, 3)
            self.step(10, '返回小红书主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
