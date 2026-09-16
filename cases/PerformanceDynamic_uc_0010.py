from aw import SeaOfStarsAW
from cases.uc_common import UcCase


class PerformanceDynamic_uc_0010(UcCase):
    """Excel 7.0.2：UC 浏览器频道和新闻浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动UC浏览器')
                self.start_uc()
            self.step(2, '左滑5次切换顶部tab栏')
            self.horizontal_browse(5, 0)
            self.step(3, '上滑5次，下滑5次浏览当前页面')
            self.browse(5, 5)
            self.step(4, '右滑5次切换顶部tab栏')
            self.horizontal_browse(0, 5)
            self.step(5, '点击体育，切换到体育页')
            self.select_channel('体育')
            self.step(6, '体育页浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(7, '点击推荐，切换到推荐页')
            self.select_channel('推荐')
            self.step(8, '点击推荐下的第一条新闻')
            self.open_first_news()
            self.step(9, '浏览新闻内容，上下各滑动5次')
            self.browse(5, 5)
            self.step(10, '返回UC浏览器主界面')
            self.return_home()
            self.step(11, '浏览首页，上下各滑动5次')
            self.browse(5, 5)
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
