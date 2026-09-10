"""iOS 电话动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class PhoneCase(WdaCase):
    PACKAGE = 'com.apple.mobilephone'
    APP_NAME = '电话'

    def __init__(self, result_path):
        super().__init__(result_path)
        self.contact_detail_open = False

    def start_phone(self):
        self.start_app(wait=4)
        self.wait_for_phone()

    def wait_for_phone(self, timeout=8):
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            if self.find('标签页栏', nodes=nodes) is not None:
                return
            if time.monotonic() >= deadline:
                self.fail('电话应用未显示标签页栏')
            time.sleep(0.5)

    def open_tab(self, name):
        self.tap(name, min_y=740, wait=2)

    def open_contact_search(self):
        # iOS 26 的通讯录页不再内置搜索框，使用电话底部“搜索”页替代。
        nodes = self.nodes()
        if not any(node.tag == 'XCUIElementTypeSearchField'
                   and node.get('visible') == 'true' for node in nodes):
            logging.warning('联系人页无搜索框，使用电话底部“搜索”作为替代')
            self.open_tab('搜索')
        deadline = time.monotonic() + 6
        while True:
            if any(node.tag == 'XCUIElementTypeSearchField'
                   and node.get('visible') == 'true' for node in self.nodes()):
                return
            if time.monotonic() >= deadline:
                self.fail('未找到电话搜索框')
            time.sleep(0.5)

    def search_contact(self, text):
        if not self.device(type='XCUIElementTypeSearchField', visible=True).exists:
            self.open_contact_search()
        field = self.device(type='XCUIElementTypeSearchField', visible=True)
        field.clear_text()
        field.set_text(text)
        time.sleep(3)

        nodes = self.nodes()
        if self.find('无结果', nodes=nodes) is not None:
            logging.warning('设备中没有联系人 %s，跳过打开联系人详情', text)
            self.contact_detail_open = False
            return False
        matches = []
        fallback_cells = []
        for node in nodes:
            name = self.node_name(node)
            y = float(node.get('y', 0))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeCell'
                    and 100 < y < 740):
                fallback_cells.append(node)
            if (node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeCell', 'XCUIElementTypeButton')
                    and text.lower() in name.lower()
                    and y < 740):
                matches.append(node)
        if not matches and fallback_cells:
            matches = fallback_cells
        if not matches:
            logging.warning('搜索结果中没有联系人 %s，跳过打开联系人详情', text)
            self.contact_detail_open = False
            return False
        matches.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(matches[0])
        time.sleep(3)
        self.contact_detail_open = True
        return True

    def return_to_contacts(self):
        if self.contact_detail_open:
            nodes = self.nodes()
            back = self.find('BackButton', '返回', contains=True, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        if self.find('关闭') is not None:
            self.tap('关闭', wait=1)
        self.open_tab('通讯录')
        self.contact_detail_open = False

    def enter_and_delete_number(self, number):
        self.open_tab('拨号键盘')
        for digit in number:
            if not self.device(label=digit).exists:
                self.fail('拨号键盘缺少数字 {}'.format(digit))
            self.device(label=digit).click()
            time.sleep(0.2)
        nodes = self.nodes()
        delete = self.find('DeleteButton', nodes=nodes)
        if delete is None:
            self.fail('输入号码后未出现删除键')
        x = round(float(delete.get('x', 0)) + float(delete.get('width', 0)) / 2)
        y = round(float(delete.get('y', 0)) + float(delete.get('height', 0)) / 2)
        for _ in number:
            self.device.click(x, y)
            time.sleep(0.2)

    def show_call_history(self):
        size = self.device.window_size()
        self.device.click(round(size.width / 2), round(size.height * 0.2))
        time.sleep(1)
        # 当前 iOS 的拨号键盘不会因点击空白处自动关闭，切回“通话”页。
        self.open_tab('通话')

    def return_phone_main(self):
        if self.find('关闭') is not None:
            self.tap('关闭', wait=1)
        self.open_tab('通话')
