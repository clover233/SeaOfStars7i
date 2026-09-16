from aw import SeaOfStarsAW
from cases.qqbrowser_common import QqBrowserCase


class PerformanceDynamic_qqliulanqi_0010(QqBrowserCase):
    """Excel 7.0.2：QQ浏览器搜索并浏览学信网。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动QQ浏览器')
                self.start_qqbrowser()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '输入学信网，点击搜索')
            self.search('学信网')
            self.step(4, '上滑2次，下滑2次浏览搜索结果')
            self.browse_page(2, 2)
            self.step(5, '点击第一个搜索结果，进入学信网官网')
            self.open_chsi_result()
            self.step(6, '上滑2次，下滑2次浏览官网')
            self.browse_page(2, 2)
            self.step(7, '点击第一条内容')
            self.open_first_chsi_content()
            self.step(8, '上滑2次，下滑2次浏览详情')
            self.browse_page(2, 2)
            self.step(9, '返回QQ浏览器主界面')
            self.return_browser_home()
            with self.capture_trace_5s(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
