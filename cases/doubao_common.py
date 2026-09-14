"""豆包动态性能用例的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class DoubaoCase(WdaCase):
    PACKAGE = 'com.bot.doubao'
    APP_NAME = '豆包'

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 12)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def _allow_expected_permission(self):
        for name in ('允许完全访问', '允许', '允许在使用 App 时访问'):
            node = self.find(name)
            if node is not None:
                self.tap_node(node)
                time.sleep(5)
                return True
        return False

    def start_doubao(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(self.PACKAGE)
            time.sleep(0.5)
        except Exception:
            pass
        self.device.app_activate(self.PACKAGE)
        time.sleep(5)
        for optional in ('以后再说', '暂不', '我知道了'):
            node = self.find(optional)
            if node is not None:
                self.tap_node(node)
                time.sleep(2)
        new_chat = self.find('创建新对话')
        if new_chat is not None:
            self.tap_node(new_chat)
            time.sleep(4)

    def _text_field(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        fields = []
        for node in nodes:
            if node.get('visible') != 'true' or node.tag != 'XCUIElementTypeTextView':
                continue
            name = self.node_name(node)
            if name.startswith('发消息') or name.startswith('输入问题或直接发送'):
                fields.append(node)
        return fields[-1] if fields else None

    def ensure_text_field(self):
        bottom = self.find('回到底部')
        if bottom is not None:
            self.tap_node(bottom)
            time.sleep(3)
        field = self._text_field()
        if field is not None:
            return field
        text_mode = self.find('文本输入')
        if text_mode is not None:
            self.tap_node(text_mode)
            time.sleep(2)
            field = self._text_field()
            if field is not None:
                return field
        self.device.click(0.43, 0.9)
        time.sleep(2)
        field = self._text_field()
        if field is None:
            self.fail('未找到豆包对话输入框')
        return field

    def input_text(self, text):
        field = self.ensure_text_field()
        self.tap_node(field)
        selector = {'type': field.tag, 'visible': True}
        name = field.get('name')
        if name:
            selector['name'] = name
        element = self.device(**selector)
        value = field.get('value') or ''
        if value and value not in ('发消息...', '输入问题或直接发送...'):
            element.clear_text()
        element.set_text(text)
        time.sleep(1)

    def _wait_for_answer(self, question, timeout=60):
        deadline = time.monotonic() + timeout
        previous = -1
        stable = 0
        while True:
            response_length = 0
            for node in self.nodes():
                if node.tag != 'XCUIElementTypeTextView':
                    continue
                name = self.node_name(node)
                if question in name:
                    response_length = max(response_length, len(name))
            if response_length > len(question) + 20:
                stable = stable + 1 if response_length == previous else 0
                if stable >= 2:
                    return
            previous = response_length
            if time.monotonic() >= deadline:
                self.fail('豆包回答超时：{}'.format(question))
            time.sleep(2)

    def ask(self, question):
        self.input_text(question)
        self.tap('Send', wait=2, timeout=8)
        time.sleep(8)
        self._wait_for_answer(question)

    def take_photo(self):
        self.tap('相机', choose='last', wait=3)
        self._allow_expected_permission()
        self.wait_for('拍摄', timeout=15)
        self.tap('拍摄', wait=4)
        self.wait_for('发送', timeout=12)

    def send_composer(self, wait=7):
        self.tap('发送', wait=wait)

    def open_photo_picker(self):
        self.tap('更多', wait=2)
        self._allow_expected_permission()
        album = self.find('相册', min_y=500)
        if album is not None:
            self.tap_node(album)
            time.sleep(5)
        self.wait_for('所有照片', timeout=15)

    def select_two_photos(self):
        for _ in range(2):
            nodes = self.nodes()
            choices = [node for node in nodes
                       if node.get('visible') == 'true'
                       and node.tag == 'XCUIElementTypeButton'
                       and self.node_name(node).startswith('未选中，照片')]
            if not choices:
                self.fail('相册中没有足够的未选照片')
            choices.sort(key=lambda node: (
                float(node.get('y', 0)), float(node.get('x', 0))))
            self.tap_node(choices[0])
            time.sleep(1)
        done = self.find('完成')
        if done is not None:
            self.tap_node(done)
            time.sleep(4)
        else:
            close = self.find('关闭', max_y=120)
            if close is None:
                self.fail('选图后未找到完成或关闭按钮')
            self.tap_node(close)
            time.sleep(4)
        self.ensure_text_field()

    def start_call(self):
        names = ('打电话', '语音通话', '电话', '开始通话')
        direct = next((node for node in self.nodes()
                       if node.get('visible') == 'true'
                       and node.tag == 'XCUIElementTypeButton'
                       and self.node_name(node) in names), None)
        if direct is None:
            self.tap('更多', wait=2)
            direct = next((node for node in self.nodes()
                           if node.get('visible') == 'true'
                           and node.tag == 'XCUIElementTypeButton'
                           and self.node_name(node) in names), None)
        if direct is None:
            self.fail('未找到豆包通话入口')
        self.tap_node(direct)
        time.sleep(7)
        self._allow_expected_permission()
        self.wait_for('挂断通话', timeout=15)

    def hang_up(self):
        self.tap('挂断通话', wait=5)
