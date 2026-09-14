from aw import SeaOfStarsAW
from cases.yuanbao_common import YuanbaoCase


class PerformanceDynamic_yuanbao_0010(YuanbaoCase):
    """Excel 7.0.2：腾讯元宝三轮问答与结果浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动腾讯元宝')
                self.start_yuanbao()
            self.step(2, '输入“什么是AI”')
            self.ask('什么是AI')
            self.step(3, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            self.step(4, '输入“华为终端的主要产品有哪些”')
            self.ask('华为终端的主要产品有哪些')
            self.step(5, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            self.step(6, '输入“介绍几款市面上主流的手机”')
            self.ask('介绍几款市面上主流的手机')
            self.step(7, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)
            self.step(8, '返回腾讯元宝主界面')
            self.return_main()
            with self.capture_trace(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
