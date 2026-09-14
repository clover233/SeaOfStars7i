from aw import SeaOfStarsAW
from cases.deepseek_common import DeepSeekCase


class PerformanceDynamic_deepseek_0010(DeepSeekCase):
    """Excel 7.0.2：连续提问并浏览 DeepSeek 回答。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动DeepSeek')
                self.start_deepseek()
            self.step(2, '点击对话框，输入什么是AI')
            self.ask('什么是AI')
            self.step(3, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            self.step(4, '点击对话框，输入华为终端的主要产品有哪些')
            self.ask('华为终端的主要产品有哪些')
            self.step(5, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            self.step(6, '点击对话框，输入介绍几款市面上主流的手机')
            self.ask('介绍几款市面上主流的手机')
            self.step(7, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            with self.capture_trace(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
