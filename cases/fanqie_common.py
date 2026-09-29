"""番茄免费小说动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class FanqieCase(WdaCase):
    PACKAGE = 'com.dragon.read'
    APP_NAME = '番茄免费小说'

    def prepare_iteration(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束番茄免费小说进程失败，继续尝试启动')
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

    def _dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '暂不', '我知道了', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def start_fanqie(self):
        self.start_app(wait=5)
        self._dismiss_optional_prompts()
        self.return_main()

    def return_main(self):
        """退出阅读/榜单等子页面，回到书城推荐首页。"""
        for _ in range(8):
            nodes = self.nodes()
            book_city = self.find('书城', min_y=730, nodes=nodes)
            if book_city is not None:
                self.tap_node(book_city)
                time.sleep(2)
                nodes = self.nodes()
                recommend = self.find('推荐', max_y=150, nodes=nodes)
                if recommend is not None:
                    self.tap_node(recommend)
                    time.sleep(2)
                return

            back = self.find(
                'reading navigation button back', '返回', 'back',
                max_y=140, contains=True, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(4, 437, 354, 437, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达番茄免费小说主界面')

    def open_bookshelf(self):
        self.tap('书架', min_y=730, wait=3)
        self.wait_for('书架', max_y=150, timeout=8)

    def open_longsheng(self):
        """打开用户已加入书架的《长生不死》。"""
        nodes = self.nodes()
        book = self.find('长生不死', contains=True, nodes=nodes)
        if book is None:
            history = self.find('历史', max_y=190, nodes=nodes)
            if history is not None:
                self.tap_node(history)
                time.sleep(2)
                nodes = self.nodes()
                book = self.find('长生不死', contains=True, nodes=nodes)
        if book is None:
            self.fail('书架中未找到已加入的《长生不死》')
        self.tap_node(book)
        time.sleep(4)
        # 有些版本先展示书籍详情，阅读页又默认隐藏导航按钮。
        for _ in range(3):
            nodes = self.nodes()
            read = self.find('继续阅读', '开始阅读', '立即阅读',
                             contains=True, nodes=nodes)
            if read is None:
                break
            self.tap_node(read)
            time.sleep(3)
        nodes = self.nodes()
        if self.find('书架', min_y=730, nodes=nodes) is not None:
            self.fail('点击书籍后仍停留在书架')
        if self.find('reading navigation button back', '上一章', '下一章',
                     contains=True, nodes=nodes) is None:
            self.device.click(201, 437)
            time.sleep(1)
            nodes = self.nodes()
        if (self.find('reading navigation button back', '上一章', '下一章',
                      contains=True, nodes=nodes) is None
                and not any(node.get('visible') == 'true'
                            and node.tag == 'XCUIElementTypeStaticText'
                            and float(node.get('y', 0)) > 130
                            and len(self.node_name(node)) > 35
                            for node in nodes)):
            self.fail('点击书籍后未进入阅读页')

    def read_pages(self, left=5, right=5):
        for _ in range(left):
            self.device.swipe(350, 437, 50, 437, 0.3)
            time.sleep(1)
        for _ in range(right):
            self.device.swipe(50, 437, 350, 437, 0.3)
            time.sleep(1)

    def leave_reader(self):
        back = self.find('reading navigation button back', '返回',
                         max_y=150, contains=True)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(3)
        self.wait_for('书架', min_y=730, timeout=8)

    def read_longsheng_cycle(self):
        self.open_bookshelf()
        self.open_longsheng()
        self.read_pages()

    def open_listen_page(self):
        self.tap('听书', max_y=170, wait=3)
        self.wait_for('听书', max_y=170, timeout=8)

    def open_full_ranking(self):
        # 首页“完本榜”只切换榜单卡片，“完整榜单”才进入榜单页面。
        self.tap('完本榜', max_y=220, wait=2)
        self.tap('完整榜单', max_y=260, wait=4)
        self.wait_for('完本榜', min_y=190, timeout=10)
        self.tap('完本榜', min_y=190, wait=2)

    def switch_ranking(self, requested, fallback):
        nodes = self.nodes()
        target = self.find(requested, min_y=190, nodes=nodes)
        if target is None:
            target = self.find(fallback, min_y=190, nodes=nodes)
            if target is None:
                self.fail('未找到榜单：{} / {}'.format(requested, fallback))
            logging.info('当前版本无%s，使用同区域的%s兼容定位', requested, fallback)
        self.tap_node(target)
        time.sleep(2)

    def browse_ranking(self):
        for start, end in ((330, 70), (70, 330)):
            for _ in range(2):
                self.device.swipe(start, 430, end, 430, 0.4)
                time.sleep(1)
        time.sleep(1)
