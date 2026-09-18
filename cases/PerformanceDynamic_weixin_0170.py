from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0170(WeixinCase):
    """Excel 7.0.2：京东购物小程序首页浏览。"""

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
            self.step(3, '点击京东购物小程序，切换到京东购物页面')
            self.open_common_mini_program(self.JD_MINI, '京东购物')
            self.step(4, '浏览京东购物首页，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(5, '返回微信主界面')
            self.close_mini_program()
            with self.capture_trace_5s(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
