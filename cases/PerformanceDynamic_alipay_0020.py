import os

from aw import SeaOfStarsAW
from cases.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0020(AlipayCase):
    # 用户指定的已有聊天对象；换设备时可以通过环境变量修改。
    CHAT_NAME = '子健'

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动支付宝')
                self.start_alipay()
            self.step(2, '首页点击tab切换理财')
            self.tap('理财')
            self.step(3, '上滑2次，下滑2次浏览理财')
            self.browse(2, 2)
            self.step(4, '点击稳健理财')
            self.tap('稳健理财')
            self.dismiss_finance_intro()
            self.step(5, '上滑2次，下滑2次浏览稳健理财')
            self.browse(2, 2)
            self.step(6, '点击稳健理财页热销的第一个理财产品')
            self.open_first_product()
            self.step(7, '上滑2次，下滑2次浏览产品')
            self.browse(2, 2)
            self.step(8, '返回理财页')
            self.return_tab('理财')
            self.step(9, '理财页点击tab切换消息')
            self.tap('消息')
            self.step(10, '点击测试账号进入聊天对话框')
            self.open_chat(os.environ.get('ALIPAY_CHAT_NAME', self.CHAT_NAME))
            self.step(11, '上滑5次，下滑5次查看聊天记录')
            self.browse(5, 5)
            self.step(12, '点击输入框，发送动态性能测试')
            self.send_chat_text('动态性能测试')
            self.step(13, '点击图片')
            self.open_chat_photos()
            self.step(14, '选择5张图片，点击完成')
            self.send_five_photos()
            self.step(15, '返回消息页')
            self.return_tab('消息')
            self.step(16, '点击右上角+号')
            self.tap('更多', '+', fallback=(0.944, 0.09))
            self.step(17, '点击扫一扫')
            # 消息菜单将图标与文字合并成一个可访问名称。
            self.tap('扫一扫', '\ue60e, 扫一扫', fallback=(0.81, 0.274))
            self.step(18, '点击相册')
            self.tap('相册')
            self.step(19, '返回消息页')
            self.return_tab('消息')
            self.step(20, '点击我的')
            self.tap('我的')
            self.step(21, '点击支付宝会员')
            self.tap('支付宝会员')
            self.step(22, '上滑5次，下滑5次浏览会员页')
            self.browse(5, 5)
            self.step(23, '返回我的页')
            self.return_tab('我的')
            self.step(24, '点击账单')
            self.tap('账单')
            self.step(25, '返回我的页')
            self.return_tab('我的')
            self.step(26, '点击余额')
            self.tap('余额')
            self.step(27, '返回我的页')
            self.return_tab('我的')
            self.step(28, '点击设置')
            self.tap('设置')
            self.step(29, '点击新消息通知')
            # 当前设置页仅导航栏可访问，列表按 weditor 实测坐标兜底。
            self.tap('新消息通知', fallback=(0.5, 0.405))
            self.step(30, '返回设置页')
            self.back()
            self.return_to('设置')
            self.step(31, '点击通用')
            self.tap('通用', fallback=(0.5, 0.638))
            self.step(32, '返回我的页')
            self.return_tab('我的')
            self.step(33, '返回支付宝主界面')
            self.return_tab('首页')
            with self.capture_trace(iteration, 34):
                self.step(34, '滑动返回Home页')
                self.launcher()
