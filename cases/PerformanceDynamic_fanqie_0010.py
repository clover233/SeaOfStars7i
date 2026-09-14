import time

from aw import SeaOfStarsAW
from cases.fanqie_common import FanqieCase


class PerformanceDynamic_fanqie_0010(FanqieCase):
    """Excel 7.0.2：浏览首页并反复阅读《长生不死》。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动番茄免费小说')
                self.start_fanqie()
            self.step(2, '首页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击书架')
            self.open_bookshelf()
            self.step(4, '点击长生不死书籍，进入阅读书籍页面')
            self.open_longsheng()
            self.step(5, '滑动阅读书籍，左翻页5次，右翻页5次')
            self.read_pages()
            self.step(6, '返回主界面，步骤4和5重复执行2次')
            self.leave_reader()
            self.return_main()
            for _ in range(2):
                self.read_longsheng_cycle()
                self.leave_reader()
                self.return_main()
            with self.capture_trace(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
