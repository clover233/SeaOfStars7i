from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0090(WeixinCase):
    """Excel 7.0.2：搜索、扫一扫与二维码收款页。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击搜索')
            self.tap('搜索', max_y=180, wait=2)
            self.step(3, '搜索华为手机')
            self.enter_text('华为手机', clear=True)
            self.tap('Search', '搜索', min_y=700, wait=4)
            self.step(4, '返回微信主界面')
            self.return_weixin_home()
            self.step(5, '点击右上角快捷操作')
            self.tap('快捷操作', max_y=120, wait=2)
            self.step(6, '点击扫一扫，进入扫码页')
            self.tap('扫一扫', wait=4)
            self.dismiss_mini_program_permissions()
            self.step(7, '返回微信主界面')
            self.return_weixin_home()
            self.step(8, '点击右上角快捷操作')
            self.tap('快捷操作', max_y=120, wait=2)
            self.step(9, '点击收付款')
            self.tap('收付款', wait=4)
            self.step(10, '点击二维码收款')
            self.tap('二维码收款', wait=4)
            self.step(11, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
