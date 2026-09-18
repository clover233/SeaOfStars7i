from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0180(WeixinCase):
    """Excel 7.0.2：同程旅行火车票结果及日期页面浏览。"""

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
            self.step(3, '点击同程旅行小程序，切换到同程旅行页面')
            self.open_common_mini_program(self.TONGCHENG_MINI)
            self.step(4, '点击火车票查询，切换到火车票页面')
            self.tongcheng_query_trains()
            self.step(5, '浏览火车票页面，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(6, '点击右上角更多日期，切换到日期界面')
            self.tongcheng_open_more_dates()
            self.step(7, '返回火车票页面')
            self.tongcheng_close_dates()
            self.step(8, '返回同程旅行页面')
            self.tongcheng_return_home()
            self.step(9, '返回微信主界面')
            self.close_mini_program()
            with self.capture_trace_5s(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
