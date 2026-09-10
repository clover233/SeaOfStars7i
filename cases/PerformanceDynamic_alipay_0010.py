from aw import SeaOfStarsAW
from cases.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0010(AlipayCase):
    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动支付宝')
                self.start_alipay()
            self.step(2, '点击出行')
            self.tap('出行', wait=3)
            self.step(3, '切换到地铁页')
            # 2026-09-09 weditor：出行网页未暴露文字控件，402×874 点屏幕。
            self.tap('地铁', fallback=(0.5, 0.258))
            self.step(4, '返回支付宝首页')
            self.return_tab('首页')
            self.step(5, '点击卡包')
            self.tap('卡包')
            self.step(6, '返回支付宝首页')
            self.return_tab('首页')
            self.step(7, '点击我的')
            self.tap('我的')
            self.step(8, '返回支付宝首页')
            self.return_tab('首页')
            self.step(9, '点击收付款')
            self.tap('收付款')
            self.step(10, '点击转账按钮')
            self.tap('转账')
            self.step(11, '点击转到银行卡')
            self.tap('转到银行卡')
            self.step(12, '返回转账页')
            self.back()
            # “转到银行卡”也会出现在子页标题中，用转账首页独有入口判断返回成功。
            self.return_to('二维码转账')
            self.step(13, '点击转到支付宝')
            self.tap('转到支付宝', '转到支付宝账户')
            self.step(14, '返回支付宝首页')
            self.return_tab('首页')
            self.step(15, '首页点击扫一扫')
            self.tap('扫一扫')
            self.step(16, '点击相册按钮')
            self.tap('相册')
            self.step(17, '点击当前页面的第一个图片，预览大图')
            self.preview_first_photo()
            self.step(18, '返回支付宝主界面')
            self.return_tab('首页')
            with self.capture_trace(iteration, 19):
                self.step(19, '滑动返回Home页')
                self.launcher()
