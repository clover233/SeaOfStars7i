"""大众点评动态性能用例的 WDA 页面能力。"""

import logging
import time

from cases.wda_case_common import WdaCase


class DianpingCase(WdaCase):
    PACKAGE = 'com.dianping.dpscope'
    APP_NAME = '大众点评'

    def _enable_continuous_ui_mode(self):
        """避免动态图文流让 XCTest 一直等待应用进入 idle。"""
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings({
                'waitForIdleTimeout': 0,
                'animationCoolOffTimeout': 0,
            })
        except Exception:
            logging.exception('WDA 不支持 idle 等待设置，继续使用默认配置')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is None:
            return
        try:
            self.device.appium_settings(previous)
        except Exception:
            logging.exception('恢复 WDA idle 等待设置失败')
        self._previous_idle_settings = None

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

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

    def _edge_back(self, wait=3):
        self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
        time.sleep(wait)

    def _is_home(self, nodes):
        return (self.find('首页', min_y=740, nodes=nodes) is not None
                and self.find('搜索按钮', max_y=180, nodes=nodes) is not None)

    def return_home(self):
        for _ in range(10):
            nodes = self.nodes()
            if self._is_home(nodes):
                return
            if self.find('福利中心', max_y=130, nodes=nodes) is not None:
                # 左侧快捷抽屉打开时，点击右侧遮罩关闭。
                self.device.click(350, 400)
                time.sleep(3)
                continue
            back = self.find('返回', 'search_back', nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                # 搜索结果 rootView 和图片预览层不响应侧滑返回，但左上角
                # 返回/关闭控件在 402×874 设备上的中心位置稳定。
                self.device.click(22, 84)
                time.sleep(3)
        self.fail('多次返回后仍未到达大众点评首页')

    def start_dianping(self):
        self._enable_continuous_ui_mode()
        self.start_app(wait=6)
        self.return_home()

    def _ensure_home_categories(self):
        """回到包含美食、景点游玩和休闲玩乐宫格的首页推荐流。"""
        self.return_home()
        for _ in range(3):
            nodes = self.nodes()
            if all(self.find(name, max_y=340, nodes=nodes) is not None
                   for name in ('美食', '景点游玩', '休闲玩乐')):
                return
            # 首页会记住“附近”等顶部频道；“上海”频道展示推荐宫格。
            recommendation = self.find('推荐', '上海', max_y=130, nodes=nodes)
            if recommendation is not None:
                self.tap_node(recommendation)
            else:
                home = self.find('首页', min_y=740, nodes=nodes)
                if home is not None:
                    self.tap_node(home)
            time.sleep(4)
        self.fail('大众点评首页未显示美食、景点游玩和休闲玩乐入口')

    def open_food(self):
        self._ensure_home_categories()
        self.tap('美食', max_y=340, wait=6)
        self.wait_for('searchbox_view', timeout=12)

    def enter_food_keyword(self, keyword):
        nodes = self.nodes()
        search_box = self.find('searchbox_view', nodes=nodes)
        if search_box is not None:
            self.tap_node(search_box)
            time.sleep(3)
        else:
            self.tap('输入商户名、地点或菜品', contains=True, wait=3)
        self.wait_for('search_keyword_edit')
        self.tap('search_keyword_edit', wait=1)
        nodes = self.nodes()
        existing = [self.node_name(node) for node in nodes
                    if node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and 60 <= float(node.get('x', 0)) < 300
                    and 70 <= float(node.get('y', 0)) < 105
                    and self.node_name(node) not in ('搜索', 'search_button')]
        current = existing[0] if existing else ''
        if current != keyword:
            delete = self.device(className='XCUIElementTypeKey', name='delete')
            for _ in range(len(current)):
                delete.click()
                time.sleep(0.1)
            self.device.send_keys(keyword)
        else:
            logging.info('搜索框已是“%s”，无需重复输入', keyword)
        time.sleep(2)

    def submit_food_search(self):
        self.tap('search_button', wait=6)
        self.wait_for('rootView', timeout=12)

    def open_first_shop(self):
        # 2026-09-11 weditor（402×874）：搜索结果由 rootView 自绘，
        # 第一家商铺图片/卡片的稳定点击区域位于 (100, 280)。
        self.device.click(100, 280)
        time.sleep(6)
        self.wait_for('返回', timeout=12)

    def open_reviews(self):
        self.tap('评价', wait=5)

    def open_all_reviews(self):
        # 店铺详情同时存在推荐菜、问大家和评价三个“查看全部”。只有出现
        # 评价筛选上下文后才点击，避免误入推荐菜或问答页面。
        review_markers = ('全部评价', '消费后评价', '最新', '有图', '好评', '差评')
        for _ in range(10):
            nodes = self.nodes()
            has_review_context = any(
                self.find(marker, contains=True, nodes=nodes) is not None
                for marker in review_markers)
            view_all = self.find('查看全部', nodes=nodes)
            if has_review_context and view_all is not None:
                self.tap_node(view_all)
                time.sleep(6)
                return
            self.device.swipe(0.5, 0.68, 0.5, 0.48, 0.25)
            time.sleep(1)

        # 某些商铺不渲染评价摘要；回到顶部后点击评分条的评价数量进入列表。
        logging.warning('店铺未渲染评价“查看全部”，使用评分条评价数量替代')
        for _ in range(8):
            self.device.swipe(0.5, 0.35, 0.5, 0.78, 0.25)
            time.sleep(0.7)
        nodes = self.nodes()
        counts = [node for node in nodes
                  if node.get('visible') == 'true'
                  and self.node_name(node).endswith('条')
                  and float(node.get('y', 0)) < 430]
        if not counts:
            self.fail('未找到评价“查看全部”或评分条评价数量')
        self.tap_node(sorted(counts, key=lambda node: float(
            node.get('y', 0)))[0])
        time.sleep(6)

    def return_to_food_page(self):
        for _ in range(7):
            nodes = self.nodes()
            if self.find('searchbox_view', nodes=nodes) is not None:
                return
            back = self.find('返回', 'search_back', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.click(22, 84)
            time.sleep(3)
        self.fail('未返回大众点评美食页面')

    def return_food_home(self):
        self.return_home()

    def open_home_category(self, name):
        self._ensure_home_categories()
        self.tap(name, max_y=340, wait=6)

    def return_from_category(self):
        nodes = self.nodes()
        if self._is_home(nodes):
            return
        back = self.find('返回', 'search_back', nodes=nodes)
        if back is not None:
            self.tap_node(back)
            time.sleep(3)
        else:
            self.device.click(22, 84)
            time.sleep(3)
        self.wait_for('首页', min_y=740, timeout=12)
