from aw import SeaOfStarsAW
from cases.tencentnews_common import TencentNewsCase


class PerformanceDynamic_tencentnews_0010(TencentNewsCase):
    """Excel 7.0.2：腾讯新闻首页和新闻详情浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动腾讯新闻')
                self.start_tencentnews()
            self.step(2, '首页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '首页浏览，左滑5次，右滑5次')
            self.horizontal_browse(5, 5)
            self.step(4, '点击查看首页新闻内容')
            self.open_first_news()
            self.step(5, '新闻页面上滑2次，下滑2次')
            self.browse(2, 2)
            with self.capture_trace_5s(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
