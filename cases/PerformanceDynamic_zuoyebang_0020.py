from aw import SeaOfStarsAW
from cases.zuoyebang_common import ZuoyebangCase


class PerformanceDynamic_zuoyebang_0020(ZuoyebangCase):
    """作业帮“成语故事”搜索结果浏览及点赞。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动作业帮')
                self.start_zuoyebang()

            self.step(2, '点击首页搜索框，进入搜索界面')
            self.focus_home_search()
            self.step(3, '输入“成语故事”并搜索')
            self.search('成语故事')
            self.step(4, '搜索结果页上滑3次、下滑3次')
            self.browse(3, 3)
            self.step(5, '点击查看更多，并上滑1次')
            self.open_more_results()
            self.browse(1, 0)
            self.step(6, '点击赞')
            self.like_result()
            self.step(7, '返回作业帮主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
