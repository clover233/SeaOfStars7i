"""iOS 备忘录动态性能用例的实机定位操作。"""

import time

from cases.wda_case_common import WdaCase


class BeiwangluCase(WdaCase):
    PACKAGE = 'com.apple.mobilenotes'
    APP_NAME = '备忘录'
    all_app_package_list = [PACKAGE]

    def start_notes(self):
        self.start_app(wait=4)
        self.return_notes_list()

    def on_notes_list(self):
        # 编辑页底部也有“新备忘录”，列表页以 SearchField“搜索”为稳定锚点。
        return any(node.get('visible') == 'true'
                   and node.tag.endswith('SearchField')
                   and self.node_name(node) == '搜索'
                   for node in self.nodes())

    def return_notes_list(self):
        for _ in range(5):
            if self.on_notes_list():
                return
            done = self.find('完成')
            if done is not None:
                self.tap_node(done)
                time.sleep(1)
            back = self.find('BackButton')
            if back is not None:
                self.tap_node(back)
                time.sleep(2)
                continue
            break
        if not self.on_notes_list():
            self.fail('未返回备忘录主界面')

    def new_note(self):
        self.tap('新备忘录', fallback=(0.87, 0.935), wait=2)

    def replace_note_text(self, text):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true' and node.tag.endswith('TextView')]
        if not fields:
            self.fail('未找到备忘录编辑区')
        field = self.device(type='XCUIElementTypeTextView', name='Note')
        field.clear_text()
        field.set_text(text)
        time.sleep(1)

    def save_note(self):
        self.tap('完成', fallback=(0.91, 0.095), wait=2)

    def open_first_note(self):
        cells = [node for node in self.nodes()
                 if node.get('visible') == 'true'
                 and node.tag.endswith('Cell')
                 and float(node.get('y', 0)) >= 190
                 and self.node_name(node) != '今天']
        if not cells:
            self.fail('备忘录列表中没有可浏览内容')
        cells.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(cells[0])
        time.sleep(3)

    def switch_to_checklist(self):
        # iOS 没有 Excel 中华为备忘录的独立“待办页”，对应能力是“核对清单”。
        editor = self.find('Note')
        if editor is not None:
            self.tap_node(editor)
            time.sleep(1)
        self.tap('核对清单', fallback=(0.28, 0.57), wait=1)

    def focus_new_checklist_item(self):
        editor = self.find('Note')
        if editor is None:
            self.fail('未找到待办输入区')
        self.tap_node(editor)
        time.sleep(1)

    def enter_checklist_item(self, text):
        self.device.send_keys(text)
        time.sleep(1)
        self.tap('Return', fallback=(0.87, 0.895), wait=1)
