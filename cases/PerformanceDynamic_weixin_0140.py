from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0140(WeixinCase):
    """Excel 7.0.2：喜茶到店取页面浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '下滑调出最近小程序页面')
            self.open_recent_mini_programs()
            self.step(3, '点击喜茶小程序，切换到喜茶页面')
            self.open_common_mini_program(self.XICHA_MINI, '喜茶')
            self.step(4, '点击到店取，切换到到店取页面')
            self.tap('到店取', min_y=500, max_y=720, wait=5)
            self.step(5, '浏览到店取页面3次并返回顶部')
            self.browse(3, 3)
            self.step(6, '返回微信主界面')
            self.close_mini_program()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
