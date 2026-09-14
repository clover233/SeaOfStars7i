from aw import SeaOfStarsAW
from cases.cloudflashpay_common import CloudFlashPayCase


class PerformanceDynamic_cloudflashpay_0010(CloudFlashPayCase):
    """Excel 7.0.2：云闪付浏览主界面、扫码和优惠分类。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动云闪付')
                self.start_cloudflashpay()
            self.step(2, '主页浏览，上下各滑动1次，循环5次')
            self.browse_cycles(5)
            self.step(3, '点击收付款')
            self.open_pay_and_return()
            self.step(4, '点击扫一扫')
            self.open_scanner()
            self.step(5, '返回云闪付首页，点击扫一扫')
            self.return_home_and_open_scanner()
            self.step(6, '点击优惠')
            self.open_discount()
            self.step(7, '浏览优惠页，上下各滑动1次，循环5次')
            self.browse_cycles(5)
            self.step(8, '点击惠生活')
            self.open_benefit_life()
            self.step(9, '浏览惠生活，上下各滑动1次')
            self.browse_cycles(1)
            self.step(10, '返回优惠页，点击美食')
            self.open_food()
            self.step(11, '返回云闪付主界面')
            self.return_home()
            with self.capture_trace(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
