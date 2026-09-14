import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_qianwen_0010(WdaCase):
    """Excel 7.0.2：连续向千问提问三次并浏览回答。"""

    PACKAGE = 'com.aliyun.ios.tongyi'
    APP_NAME = '千问'

    def dismiss_notification_alert(self):
        if self.device(label='不允许').exists:
            self.device(label='不允许').click()
            time.sleep(3)

    def new_chat(self):
        nodes = self.nodes()
        button = self.find('ty_main_chat_sidebar_new_chat_button', nodes=nodes)
        if button is None:
            self.tap('ty_main_chat_top_bar_left_menu_button', wait=2)
            button = self.find('ty_main_chat_sidebar_new_chat_button')
        if button is None:
            self.fail('未找到千问“新建对话”入口')
        self.tap_node(button)
        time.sleep(4)

    def input_field(self):
        nodes = self.nodes()
        field = self.find('qkn_chat_input_text_field', nodes=nodes)
        if field is None:
            # 未聚焦时输入框由自绘容器呈现。
            self.device.click(0.45, 0.91)
            time.sleep(2)
            field = self.find('qkn_chat_input_text_field')
        if field is None:
            self.fail('未找到千问对话框')
        return field

    def ask(self, text):
        node = self.input_field()
        field = self.device(
            type='XCUIElementTypeTextView',
            name=self.node_name(node),
            visible=True,
        )
        current = node.get('value') or ''
        if current and current not in ('发消息...', '发消息或按住说话...'):
            field.clear_text()
        field.set_text(text)
        time.sleep(1)
        self.tap('qkn_chat_input_send_btn', wait=2, timeout=8)

        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            nodes = self.nodes()
            question_sent = self.find(text, nodes=nodes) is not None
            answer_complete = self.find(
                'qkn_chat_latest_answer_complete', nodes=nodes) is not None
            if question_sent and answer_complete:
                return
            time.sleep(2)
        self.fail('千问回答超时：{}'.format(text))

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动千问')
                self.start_app(wait=5)
            self.dismiss_notification_alert()
            self.new_chat()

            self.step(2, '点击对话框，输入什么是AI')
            self.ask('什么是AI')

            self.step(3, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)

            self.step(4, '点击对话框，输入华为终端的主要产品有哪些')
            self.ask('华为终端的主要产品有哪些')

            self.step(5, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)

            self.step(6, '点击对话框，输入介绍几款市面上主流的手机')
            self.ask('介绍几款市面上主流的手机')

            self.step(7, '浏览搜索结果，上下滑动3次')
            self.browse(3, 3)

            self.step(8, '返回千问主界面')
            self.new_chat()

            with self.capture_trace(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
