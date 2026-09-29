"""DeepSeek 动态性能用例的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class DeepSeekCase(WdaCase):
    PACKAGE = 'com.deepseek.chat'
    APP_NAME = 'DeepSeek'

    def wait_for_text_view(self, timeout=12):
        deadline = time.monotonic() + timeout
        while True:
            fields = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and node.get('enabled') != 'false'
                      and node.tag == 'XCUIElementTypeTextView'
                      and float(node.get('y', 0)) >= 300
                      and 0 < float(node.get('height', 0)) <= 180]
            if fields:
                return fields[-1]
            if time.monotonic() >= deadline:
                self.fail('未找到 DeepSeek 对话框')
            time.sleep(0.5)

    def start_deepseek(self):
        self.start_app(wait=6)
        nodes = self.nodes()
        start = self.find('开始对话', nodes=nodes)
        if start is not None:
            self.tap_node(start)
            time.sleep(4)
        nodes = self.nodes()
        new_chat = self.find('sessionNewChatButton', nodes=nodes)
        if new_chat is not None:
            self.tap_node(new_chat)
            time.sleep(3)
        self.wait_for_text_view()

    def ask(self, text):
        node = self.wait_for_text_view()
        self.tap_node(node)
        # 回答正文也是 TextView；无名称时仅用 type/visible 会选中正文。
        # 键盘弹出后输入栏仍位于 y>=300，且高度远小于回答容器。
        field = self.device(xpath="//XCUIElementTypeTextView[@visible='true' "
                            "and @enabled='true' and @y >= 300 and @height <= 180]")
        value = node.get('value') or ''
        if value and value != '发消息或按住说话':
            field.clear_text()
        field.set_text(text)
        time.sleep(1)
        self.tap('发送', wait=1, timeout=8)

        time.sleep(8)
        deadline = time.monotonic() + 37
        while True:
            nodes = self.nodes()
            sending = self.find('发送', nodes=nodes)
            voice = self.find('voice', nodes=nodes)
            if sending is None and voice is not None:
                return
            if time.monotonic() >= deadline:
                self.fail('DeepSeek 回答超时：{}'.format(text))
            time.sleep(2)
