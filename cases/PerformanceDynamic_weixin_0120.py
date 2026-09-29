from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0120(WeixinCase):
    """Excel 7.0.2：微信红包页面及转账说明。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击测试账号，进入好友聊天页面')
            self.open_chat(self.TEST_ACCOUNT)
            self.step(3, '点击加号，进入更多功能页面')
            self.open_chat_actions()
            self.step(4, '点击红包，进入红包页面后返回上一页面')
            self.tap('红包', min_y=650, wait=3)
            self.edge_back(wait=2)
            self.step(5, '点击加号，进入更多功能页面')
            self.open_chat_actions()
            self.step(6, '点击转账，进入转账页面')
            self.tap('转账', min_y=650, wait=4)
            self.enter_transfer_page()
            self.step(7, '点击添加转账说明，进入添加说明页面')
            self.tap('添加转账说明', '添加说明', contains=True, wait=2)
            self.step(8, '输入修改')
            self.enter_text('修改', clear=True)
            self.step(9, '点击确定，进入转账页面')
            self.tap('确定', min_y=350, max_y=520, wait=3)
            self.step(10, '返回好友聊天页面')
            self.edge_back(wait=2)
            self.step(11, '下滑3次浏览好友聊天页面')
            self.chat_swipe_down(3)
            self.step(12, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 13):
                self.step(13, '滑动返回Home页')
                self.launcher()
