import time

from aw import SeaOfStarsAW
from cases.qimao_common import QimaoCase


class PerformanceDynamic_qimao_0010(QimaoCase):
    """Excel 7.0.2：从书架阅读《狂飙》并往返翻页。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动七猫免费小说')
                self.start_qimao()
            self.step(2, '点击书架，进入书架页面')
            self.tap('书架', min_y=760, wait=3)
            self.step(3, '点击狂飙书籍进行阅读')
            self.tap('狂飙', min_y=120, max_y=700, wait=4)
            self.step(4, '阅读书籍页面，向左翻页5次，向右翻页5次')
            self.turn_pages(5, 5)
            self.step(5, '返回七猫免费小说主界面')
            self.return_book_city()
            with self.capture_trace(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
