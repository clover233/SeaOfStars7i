"""腾讯元宝动态性能用例的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class YuanbaoCase(WdaCase):
    PACKAGE = 'com.tencent.hunyuan.app.chat'
    APP_NAME = '腾讯元宝'

    def _dismiss_optional_popup(self):
        nodes = self.nodes()
        close = self.find('ic kouling close', nodes=nodes)
        if close is not None:
            self.tap_node(close)
            time.sleep(4)

    def start_yuanbao(self):
        self.start_app(wait=7)
        self._dismiss_optional_popup()
        nodes = self.nodes()
        new_chat = self.find('新建对话', nodes=nodes)
        if new_chat is not None:
            self.tap_node(new_chat)
            time.sleep(4)

    def ask(self, text):
        self.device.click(170, 760)
        time.sleep(1)
        self.device.send_keys(text)
        time.sleep(1)
        send = self.find('Send')
        if send is None:
            self.fail('系统键盘未出现发送键')
        self.tap_node(send)
        time.sleep(12)
        if self.find(text, contains=True) is None:
            self.fail('元宝未显示已发送问题：{}'.format(text))

    def return_main(self):
        nodes = self.nodes()
        new_chat = self.find('新建对话', nodes=nodes)
        if new_chat is not None:
            self.tap_node(new_chat)
            time.sleep(4)
        if self.find('Hi，今天从哪里开始？', contains=True) is None:
            self.fail('未返回腾讯元宝主界面')
