from aw import SeaOfStarsAW
from cases.uc_common import UcCase


class PerformanceDynamic_uc_0020(UcCase):
    """Excel 7.0.2：UC 浏览器搜索和搜索发现浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动UC浏览器')
                self.start_uc()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '输入大话天仙，进行搜索')
            self.search('大话天仙')
            self.step(4, '上下各滑动5次浏览搜索结果')
            self.browse(5, 5)
            self.step(5, '返回搜索页面')
            self.return_search_page()
            self.step(6, '点击第一条搜索发现')
            self.open_first_search_discovery()
            self.step(7, '上下滑动各5次浏览详情')
            self.browse(5, 5)
            self.step(8, '返回UC浏览器主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
