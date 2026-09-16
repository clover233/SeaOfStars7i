from aw import SeaOfStarsAW
from cases.jrtt_common import JrttCase


class PerformanceDynamic_jrtt_0010(JrttCase):
    """浏览推荐、热榜及文章。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动今日头条')
                self.start_jrtt()
            self.step(2, '主页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击热榜tab')
            self.tap('热榜', max_y=140, wait=5)
            self.step(4, '热榜上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(5, '点击热榜第一条')
            self.open_first_feed_item()
            self.step(6, '热榜第一条上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(7, '返回热榜页面')
            self.edge_back()
            self.step(8, '返回推荐页，点击第一条文章')
            self.tap('推荐', contains=True, max_y=140, wait=3)
            self.open_first_feed_item()
            self.step(9, '文章页上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(10, '返回今日头条主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
