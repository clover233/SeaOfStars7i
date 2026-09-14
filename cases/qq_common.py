"""QQ 动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class QqCase(WdaCase):
    PACKAGE = 'com.tencent.mqq'
    APP_NAME = 'QQ'

    def prepare_iteration(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        self.device.app_terminate(self.PACKAGE)
        time.sleep(1)

    def wait_for(self, *names, **kwargs):
        timeout = kwargs.pop('timeout', 10)
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            node = self.find(*names, nodes=nodes, **kwargs)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('未进入预期页面：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def dismiss_optional_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            prompt = self.find(
                '不允许', '以后再说', '暂不', '我知道了', '关闭',
                '要求 App 不跟踪', '保留当前选择', nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(1)

    def edge_back(self):
        self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(2)

    @staticmethod
    def _is_fullscreen_image(node):
        return (node.tag == 'XCUIElementTypeImage'
                and float(node.get('width', 0)) >= 390
                and float(node.get('height', 0)) >= 840)

    def bottom_tab(self, text, nodes=None):
        matches = self.matching_nodes(
            text, contains=True, min_y=740, nodes=nodes)
        return matches[0] if matches else None

    def return_message_home(self):
        for _ in range(10):
            nodes = self.nodes()
            message = self.bottom_tab('消息', nodes=nodes)
            if message is not None:
                self.tap_node(message)
                time.sleep(3)
                return
            fullscreen = next(
                (node for node in nodes if node.get('visible') == 'true'
                 and self._is_fullscreen_image(node)), None)
            if fullscreen is not None:
                # 2026-09-14 weditor（402×874）：QQ 图片查看器无返回节点，
                # 单击图片可关闭查看器并回到来源页面。
                self.device.click(201, 437)
                time.sleep(3)
                continue
            back = self.find('返回', max_y=140, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self.edge_back()
        self.fail('多次返回后仍未到达 QQ 消息主界面，请确认账号已登录')

    def start_qq(self):
        self.start_app(wait=6)
        self.dismiss_optional_prompts()
        self.return_message_home()
        if self.find('账户及设置') is None:
            self.fail('QQ 未处于登录状态，请预先登录测试账号')

    def swipe_images(self, right, left):
        for start, end, count in ((0.18, 0.82, right), (0.82, 0.18, left)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.3)
                time.sleep(1)
        time.sleep(1)

    def open_space_picture(self):
        for attempt in range(5):
            nodes = self.nodes()
            pictures = [node for node in nodes
                        if node.get('visible') == 'true'
                        and node.tag == 'XCUIElementTypeImage'
                        and self.node_name(node) == '图片'
                        and 120 <= float(node.get('y', 0)) <= 760
                        and float(node.get('width', 0)) >= 80
                        and float(node.get('height', 0)) >= 80]
            if pictures:
                pictures.sort(key=lambda node: (
                    float(node.get('y', 0)), float(node.get('x', 0))))
                self.tap_node(pictures[0])
                time.sleep(5)
                self.wait_for('第1张图片', contains=True, timeout=10)
                return
            if attempt < 4:
                self.device.swipe(0.5, 0.72, 0.5, 0.35, 0.3)
                time.sleep(2)
        self.fail('空间动态中未找到好友发布的图片说说')

    def open_picture_message(self):
        nodes = self.nodes()
        messages = [node for node in nodes
                    if node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeOther'
                    and '图片' in self.node_name(node)
                    and 100 <= float(node.get('y', 0)) <= 720
                    and float(node.get('height', 0)) >= 80]
        if not messages:
            self.fail('当前聊天页没有可查看的图片消息')
        messages.sort(key=lambda node: float(node.get('y', 0)))
        message = messages[-1]
        name = self.node_name(message)
        y = max(170, min(700, round(
            float(message.get('y', 0)) + float(message.get('height', 0)) / 2)))
        # 消息气泡整体可访问，但图片本身不单独暴露；发出消息靠右，收到消息靠左。
        x = 290 if name.startswith('我') else 112
        logging.info('使用 weditor 核对的聊天图片区域：(%s, %s)', x, y)
        self.device.click(x, y)
        time.sleep(5)
        nodes = self.nodes()
        if not any(node.get('visible') == 'true'
                   and self._is_fullscreen_image(node) for node in nodes):
            self.fail('点击图片消息后未进入大图查看器')

    def open_chat_from_message_list(self, *names):
        nodes = self.nodes()
        chat = self.find(*names, contains=True, min_y=130, max_y=760,
                         nodes=nodes)
        if chat is None:
            self.fail('消息列表未找到聊天：{}'.format(' / '.join(names)))
        self.tap_node(chat)
        time.sleep(5)

    def return_to_message_list(self):
        for _ in range(4):
            nodes = self.nodes()
            if self.find('搜索', max_y=180, nodes=nodes) is not None:
                return
            fullscreen = next(
                (node for node in nodes if node.get('visible') == 'true'
                 and self._is_fullscreen_image(node)), None)
            if fullscreen is not None:
                self.device.click(201, 437)
                time.sleep(3)
            else:
                self.edge_back()
        self.fail('侧滑后未返回 QQ 消息列表')

    def send_text_message(self, text):
        field = self.wait_for('消息', timeout=8)
        self.tap_node(field)
        time.sleep(1)
        self.enter_text(text, clear=True)
        self.tap('Send', min_y=700, wait=4)

    def send_classic_emoji(self):
        self.tap('表情', min_y=450, wait=3)
        self.tap('微笑', '花痴', min_y=580, wait=2)
        self.tap('发送', min_y=740, wait=4)

    def send_first_photo(self):
        self.tap('照片', min_y=450, wait=4)
        self.dismiss_optional_prompts()
        nodes = self.nodes()
        choices = self.matching_nodes(
            '未选中 图片', contains=True, min_y=130, max_y=760,
            nodes=nodes)
        if not choices:
            self.fail('相册中没有可发送的图片，请检查照片权限和测试图片预置')
        self.tap_node(choices[0])
        time.sleep(2)
        self.tap('发送 (1)', contains=True, min_y=740, wait=6)
