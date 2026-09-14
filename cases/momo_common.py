"""MOMO 陌陌动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class MomoCase(WdaCase):
    PACKAGE = 'com.wemomo.momoappdemo1'
    APP_NAME = 'MOMO陌陌'

    def _dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            button = self.find('好的', '我知道了', '以后再说', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(3)

    def start_momo(self):
        self.start_app(wait=7)
        self._dismiss_optional_prompts()
        self.open_tab('首页')

    def open_tab(self, name):
        nodes = self.nodes()
        tab = self.find(name, min_y=780, nodes=nodes)
        if tab is None:
            self.fail('未找到陌陌底部“{}”tab'.format(name))
        self.tap_node(tab)
        time.sleep(5)
        self._dismiss_optional_prompts()

    def open_first_live(self):
        nodes = self.nodes()
        masks = self.matching_nodes('ml_live_index_cell_mask', nodes=nodes)
        if masks:
            self.tap_node(masks[0])
        else:
            logging.warning('首个直播卡片未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(100, 270)
        time.sleep(15)

    def return_live_list(self):
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(5)
        if self.find('直播', min_y=780) is None:
            self.fail('未返回陌陌直播列表')
