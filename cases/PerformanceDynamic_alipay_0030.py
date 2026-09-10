import time

from aw import SeaOfStarsAW
from cases.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0030(AlipayCase):
    """Excel 7.0.2 模型：支付宝搜索闪送并浏览小程序。"""

    def require_shansong_page(self, *anchors):
        for _ in range(6):
            nodes = self.nodes()
            self.require_no_alert(nodes)
            if self.find('支付宝授权登录', '短信验证码登录', nodes=nodes) is not None:
                self.fail('闪送尚未登录，请先在手机上登录闪送再运行用例')
            if self.find('暂不同意', nodes=nodes) is not None:
                self.fail('请先在闪送小程序中处理首次使用协议，再运行用例')
            if self.find(*anchors, nodes=nodes) is not None:
                return
            time.sleep(1)
        self.fail('未进入预期闪送页面：{}'.format(' / '.join(anchors)))

    def search_shansong(self):
        self.tap('搜索框')
        self.require_no_alert()
        fields = [n for n in self.nodes()
                  if n.tag.endswith('TextField') and n.get('visible') == 'true']
        if not fields:
            self.fail('未找到支付宝搜索输入框')
        field = self.device(type='XCUIElementTypeTextField', visible=True)
        field.clear_text()
        time.sleep(1)
        field.set_text('闪送')
        time.sleep(1)
        self.tap('搜索', wait=3)

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动支付宝')
                self.start_alipay()
            self.step(2, '点击搜索框，输入【闪送】并确定')
            self.search_shansong()
            self.step(3, '上滑1次，下滑1次，查看闪送搜索结果')
            self.browse(1, 1)
            self.step(4, '点击第一个搜索结果进入闪送小程序')
            # weditor 2026-09-09：搜索结果卡片未暴露控件；坐标指向首个小程序标题。
            self.tap('闪送', fallback=(0.24, 0.36), wait=5)
            self.require_shansong_page('帮取送')
            self.step(5, '上滑1次，下滑1次，浏览小程序信息')
            self.browse(1, 1)
            self.step(6, '点击订单，切换到订单页面')
            self.tap('订单', fallback=(0.625, 0.943))
            self.require_shansong_page('进行中', '无订单记录')
            self.step(7, '点击我的，切换到我的信息界面')
            self.tap('我的', fallback=(0.875, 0.943))
            self.require_shansong_page('常用功能', '发单偏好')
            self.step(8, '点击首页，返回小程序首页')
            self.tap('首页', fallback=(0.125, 0.943))
            self.require_shansong_page('帮取送')
            self.step(9, '侧滑返回支付宝首页')
            self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
            self.return_tab('首页')
            with self.capture_trace(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
