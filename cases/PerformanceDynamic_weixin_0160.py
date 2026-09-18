from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0160(WeixinCase):
    """Excel 7.0.2：蜜雪冰城点餐页面浏览。"""

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
            self.step(3, '点击蜜雪冰城小程序，切换到蜜雪冰城页面')
            self.open_common_mini_program(self.MIXUE_MINI)
            self.step(4, '点击点餐，切换到点餐页面')
            self.enter_mixue_order_page()
            self.step(5, '浏览点餐页面，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(6, '返回微信主界面')
            self.close_mini_program()
            with self.capture_trace_5s(iteration, 7):
                self.step(7, '滑动返回Home页')
                self.launcher()
