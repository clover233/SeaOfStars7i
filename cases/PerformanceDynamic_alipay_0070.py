from aw import SeaOfStarsAW
from cases.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0070(AlipayCase):
    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动支付宝')
                self.start_alipay()
            self.step(2, '点击医疗健康')
            self.tap('医疗健康', wait=3)
            self.step(3, '返回支付宝首页')
            self.return_tab('首页')
            self.step(4, '第二次点击医疗健康')
            self.tap('医疗健康', wait=3)
            self.step(5, '上滑1次，浏览医疗健康页面')
            self.browse(1, 0)
            self.step(6, '下滑1次，浏览医疗健康页面')
            self.browse(0, 1)
            self.step(7, '返回支付宝首页')
            self.return_tab('首页')
            self.step(8, '点击蚂蚁森林')
            self.tap('蚂蚁森林', wait=3)
            self.step(9, '上滑1次，浏览蚂蚁森林页面')
            self.browse(1, 0)
            self.step(10, '下滑1次，浏览蚂蚁森林页面')
            self.browse(0, 1)
            self.step(11, '返回支付宝首页')
            self.return_tab('首页')
            self.step(12, '点击淘宝闪购')
            # weditor 核对新布局：已加入首页宫格，按名称获取实时位置。
            self.tap('淘宝闪购', '闪购', wait=3)
            self.step(13, '上滑3次，下滑3次，浏览淘宝闪购页面')
            self.browse(3, 3)
            self.step(14, '返回支付宝主界面')
            self.return_tab('首页')
            with self.capture_trace(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
