"""钉钉及其跨应用会议场景的 WDA 页面能力。"""

import time

from cases.wda_case_common import WdaCase


class DingTalkCase(WdaCase):
    PACKAGE = 'com.laiwang.DingTalk'
    TOUTIAO_PACKAGE = 'com.ss.iphone.article.News'
    APP_NAME = '钉钉'

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

    def _restart(self, package, wait=5):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(package)
            time.sleep(0.5)
        except Exception:
            pass
        self.device.app_activate(package)
        time.sleep(wait)

    def _edge_back(self, wait=3):
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(wait)

    def start_dingtalk(self):
        self._restart(self.PACKAGE)
        self.return_messages()

    def return_messages(self):
        for _ in range(7):
            nodes = self.nodes()
            message_tab = self.find('消息', min_y=750, nodes=nodes)
            workbench = self.find('工作台', min_y=750, nodes=nodes)
            if message_tab is not None and workbench is not None:
                self.tap_node(message_tab)
                time.sleep(3)
                return
            back = self.find('返回', nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self._edge_back()
        self.fail('多次返回后仍未到达钉钉消息主页')

    def open_welcome_group(self):
        self.tap('欢迎试用钉钉群', contains=True, wait=4)
        self.wait_for('群聊信息')

    def send_group_text(self, text):
        self.tap('发消息或按住说话...', contains=True, fallback=(0.45, 0.88), wait=1)
        self.device.send_keys(text)
        time.sleep(1)
        self.tap('Send', wait=3)

    def open_group_info(self):
        self.tap('群聊信息', wait=4)
        self.wait_for('群设置')

    def open_more_panel(self):
        self.tap('更多', min_y=750, wait=3)

    def open_meeting_tab(self):
        self.tap('会议', min_y=750, wait=4)
        self.wait_for('发起会议')

    def start_voice_meeting(self):
        self.tap('发起会议', max_y=260, wait=2)
        self.tap('语音会议', wait=4)
        self.wait_for('进入会议')

    def enter_meeting(self):
        self.tap('进入会议', '入会', wait=6)
        self.wait_for('结束', max_y=150, timeout=15)

    def start_toutiao(self):
        self._restart(self.TOUTIAO_PACKAGE, wait=6)
        for optional in ('以后再说', '暂不', '我知道了'):
            node = self.find(optional)
            if node is not None:
                self.tap_node(node)
                time.sleep(2)
        self.return_toutiao_home()
        self.tap_headline_channel('推荐')

    def _headline_channel(self, name, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        channel = self.find(name, max_y=180, nodes=nodes)
        if channel is not None:
            return channel
        return self.find('已选中，{}'.format(name), max_y=180, nodes=nodes)

    def tap_headline_channel(self, name):
        node = self._headline_channel(name)
        if node is None:
            self.fail('今日头条未找到{}频道'.format(name))
        self.tap_node(node)
        time.sleep(5)

    def return_toutiao_home(self):
        for _ in range(6):
            nodes = self.nodes()
            home = self.find('首页', min_y=740, nodes=nodes)
            recommendation = self._headline_channel('推荐', nodes=nodes)
            if home is not None and recommendation is not None:
                self.tap_node(home)
                time.sleep(3)
                return
            self._edge_back()
        self.fail('多次返回后仍未到达今日头条主页')

    def open_first_headline(self, channel):
        nodes = self.nodes()
        candidates = []
        for node in nodes:
            if node.get('visible') != 'true' or node.tag != 'XCUIElementTypeStaticText':
                continue
            x = float(node.get('x', 0))
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            height = float(node.get('height', 0))
            name = self.node_name(node)
            if channel == '热榜':
                matched = x >= 40 and 200 < y < 730 and width > 120 and height >= 20
            else:
                matched = x <= 25 and 145 < y < 730 and width > 150 and height >= 20
            if matched and name not in ('实时更新', '搜索'):
                candidates.append(node)
        if not candidates:
            self.fail('{}频道未找到第一条内容'.format(channel))
        candidates.sort(key=lambda item: (float(item.get('y', 0)), float(item.get('x', 0))))
        self.tap_node(candidates[0])
        time.sleep(6)

    def activate_dingtalk_meeting(self):
        self.device.app_activate(self.PACKAGE)
        time.sleep(6)
        if self.find('结束', max_y=150) is not None:
            return
        enter = self.find('进入会议', '入会')
        if enter is not None:
            self.tap_node(enter)
            time.sleep(6)
            return
        nodes = self.nodes()
        meeting_tab = self.find('会议', min_y=750, nodes=nodes)
        if meeting_tab is not None:
            self.tap_node(meeting_tab)
            time.sleep(4)
        nodes = self.nodes()
        meetings = [node for node in nodes
                    if node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and '发起的' in self.node_name(node)
                    and '会议' in self.node_name(node)
                    and float(node.get('y', 0)) > 380]
        if meetings:
            meetings.sort(key=lambda node: float(node.get('y', 0)))
            self.tap_node(meetings[0])
            time.sleep(4)
        enter = self.find('进入会议', '入会')
        if enter is not None:
            self.tap_node(enter)
            time.sleep(6)
        self.wait_for('结束', max_y=150, timeout=15)

    def end_meeting(self):
        self.tap('结束', max_y=150, wait=2)
        everyone = self.find('全员结束会议')
        if everyone is not None:
            self.tap_node(everyone)
            time.sleep(5)

    def return_dingtalk_main(self):
        for _ in range(6):
            nodes = self.nodes()
            message_tab = self.find('消息', min_y=750, nodes=nodes)
            if message_tab is not None:
                self.tap_node(message_tab)
                time.sleep(3)
                return
            back = self.find('返回', '关闭', nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self._edge_back()
        self.fail('会议结束后未返回钉钉主界面')
