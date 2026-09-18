from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0110(WeixinCase):
    """Excel 7.0.2：钱包、手机充值、生活缴费与收藏。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击我')
            self.tap('我', min_y=760, wait=2)
            self.step(3, '点击服务')
            self.tap('服务', min_y=100, max_y=600, wait=4)
            self.step(4, '点击钱包')
            self.tap('钱包', contains=True, max_y=240, wait=4)
            self.step(5, '点击零钱')
            self.tap('balance_cell', wait=4)
            self.step(6, '返回服务页')
            self.return_service_page()
            self.step(7, '点击手机充值')
            self.tap('手机充值', wait=5)
            self.accept_payment_prompts()
            self.step(8, '返回服务页')
            self.return_service_page()
            self.step(9, '点击生活缴费')
            self.tap('生活缴费', wait=5)
            self.prepare_utility_city()
            self.step(10, '点击电费')
            self.tap('电费', wait=5)
            self.step(11, '点击第一个缴费单位')
            self.select_first_utility_company()
            self.step(12, '返回我的页面')
            self.return_me_page()
            self.step(13, '点击收藏')
            self.tap('收藏', min_y=100, max_y=700, wait=4)
            self.step(14, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
