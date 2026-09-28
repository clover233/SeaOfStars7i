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
        self.tap('发消息或按住说话', contains=True, min_y=400, wait=1)
        if not any(node.tag == 'XCUIElementTypeKeyboard'
                   and node.get('visible') == 'true' for node in self.nodes()):
            self.fail('点击输入提示后系统键盘未弹出')
        self.device.send_keys(text)
        time.sleep(1)
        self.tap('Send', '发送', min_y=600, wait=1)
        deadline = time.monotonic() + 8
        while not any(self.node_name(node) == text and
                      node.tag not in ('XCUIElementTypeTextView', 'XCUIElementTypeTextField')
                      for node in self.nodes()):
            if time.monotonic() >= deadline:
                self.fail('元宝未显示已发送问题：{}'.format(text))
            time.sleep(0.5)
        time.sleep(12)

    def return_main(self):
        nodes = self.nodes()
        new_chat = self.find('新建对话', nodes=nodes)
        if new_chat is not None:
            self.tap_node(new_chat)
            time.sleep(4)
        if self.find('Hi，今天从哪里开始？', '我是元宝，聊天、写作、搜索都在行',
                     contains=True) is None:
            self.fail('未返回腾讯元宝主界面')
