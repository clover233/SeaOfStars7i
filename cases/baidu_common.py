"""百度及百度地图动态性能用例的实机定位操作。"""

import logging
import time

from cases.wda_case_common import WdaCase


class BaiduCase(WdaCase):
    PACKAGE = 'com.baidu.BaiduMobile'
    APP_NAME = '百度'
    all_app_package_list = [PACKAGE]

    def start_baidu(self):
        self.start_app(wait=4)
        self.return_baidu_home()

    def return_baidu_home(self):
        for _ in range(7):
            if self.find('SearchBox_test') is not None and self.find('百度') is not None:
                return
            close = self.find('landing close')
            if close is not None:
                self.tap_node(close)
            else:
                back = self.find('返回', '返回按钮', '返回上一页')
                if back is not None:
                    self.tap_node(back)
                else:
                    self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        self.fail('未返回百度主界面')

    def open_wenxin(self):
        # 26.6.1 实机：界面文案是“文心一言”，无障碍名称为 AITab。
        self.tap('AITab', '文心一言', fallback=(0.5, 0.935), wait=3)

    def ask_wenxin(self, question):
        self.tap('问我问题或按住说话', fallback=(0.45, 0.925), wait=1)
        self.enter_text(question)
        self.tap('Send', '发送', 'input send', fallback=(0.87, 0.895), wait=5)

    def open_first_baike_result(self):
        matches = self.matching_nodes('百度百科', contains=True, min_y=110)
        matches = [node for node in matches if not node.tag.endswith('TextField')]
        if matches:
            self.tap_node(matches[0])
            time.sleep(5)
            return
        logging.warning('搜索结果标题未暴露，使用 weditor 核对的第一条结果区域')
        self.device.click(0.5, 0.34)
        time.sleep(5)


class BaiduMapCase(WdaCase):
    PACKAGE = 'com.baidu.map'
    APP_NAME = '百度地图'
    all_app_package_list = [PACKAGE]

    def start_baidu_map(self):
        self.start_app(wait=5)
        self.return_map_home()

    def return_map_home(self):
        for _ in range(7):
            if self.find('searchButton') is not None:
                return
            back = self.find('返回首页', '返回按钮', '返回')
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            time.sleep(2)
        self.fail('未返回百度地图主界面')

    def search_clock_tower(self):
        self.tap('searchButton', '搜地点、查公交、找路线', fallback=(0.45, 0.09), wait=1)
        self.enter_text('钟楼', clear=True)
        self.tap('Search', '搜索', fallback=(0.87, 0.895), wait=6)

    def select_xian_clock_tower(self):
        city = self.find('西安市', min_y=350, max_y=470)
        if city is not None:
            self.tap_node(city)
            time.sleep(5)
        result = self.find('西安钟楼', min_y=430, max_y=700)
        if result is None:
            result = self.find('西安', min_y=430, max_y=700)
        if result is not None:
            self.tap_node(result)
            time.sleep(5)
            return
        self.fail('搜索结果中未找到西安钟楼')

    def go_to_destination(self):
        self.tap('到这去', fallback=(0.83, 0.94), wait=6, choose='last')

    def start_navigation(self):
        self.tap('driveNaviBt', '开始导航', fallback=(0.8, 0.94), wait=2)
        nodes = self.nodes()
        names = {self.node_name(node) for node in nodes if node.get('visible') == 'true'}
        if {'拒绝', '接受'} <= names:
            # 仅处理点击“开始导航”后出现的百度地图导航使用提示。
            self.tap_node(self.find('接受', nodes=nodes))
            time.sleep(7)
        if self.find('退出') is None:
            self.fail('点击开始导航后未进入导航页')

    def exit_navigation(self):
        self.tap('退出', fallback=(0.87, 0.93), wait=2)
        self.tap('退出导航', fallback=(0.72, 0.93), wait=6)
