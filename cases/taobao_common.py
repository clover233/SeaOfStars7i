"""淘宝动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class TaobaoCase(WdaCase):
    PACKAGE = 'com.taobao.taobao4iphone'
    APP_NAME = '淘宝'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只在首尾步骤采集，并保证采样窗口不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束淘宝进程失败，继续尝试启动')
        time.sleep(1)

    def wait_for(self, *names, timeout=10, contains=False, min_y=None,
                 max_y=None):
        deadline = time.monotonic() + timeout
        while True:
            self.ensure_in_taobao()
            node = self.find(*names, contains=contains, min_y=min_y,
                             max_y=max_y)
            if node is not None:
                return node
            if time.monotonic() >= deadline:
                self.fail('等待控件超时：{}'.format(' / '.join(names)))
            time.sleep(0.5)

    def ensure_in_taobao(self):
        current = self.device.app_current().get('bundleId')
        if current != self.PACKAGE:
            self.fail('淘宝跳转到了外部应用 {}，请完成授权后返回淘宝再运行'.format(
                current or '未知应用'))

    def fail_if_security_verification(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('验证码拦截', nodes=nodes) is not None or
                self.find('亲，请拖动下方滑块完成验证', contains=True,
                          nodes=nodes) is not None or
                self.find('验证失败', contains=True, nodes=nodes) is not None):
            self.fail('触发淘宝滑块验证码，请先人工完成验证再运行')

    def fail_if_login_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('获取短信验证码', nodes=nodes) is not None or
                self.find('支付宝登录', contains=True, nodes=nodes) is not None):
            self.fail('淘宝账号未登录，请先登录测试账号再运行')

    def fail_if_chat_login_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('聊天账号下线通知', nodes=nodes) is not None or
                self.find('重登', nodes=nodes) is not None):
            self.fail('淘宝聊天账号已下线，请先点“重登”并完成客服账号登录')

    def dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            self.fail_if_security_verification(nodes)
            button = self.find('不允许', '以后再说', '暂不', '我知道了',
                               nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_taobao(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_home(select_recommend=False)

    def edge_back(self, wait=3):
        nodes = self.nodes()
        back = self.find('返回', '返回，按钮', '返回。按钮',
                         max_y=150, nodes=nodes)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_home(self, select_recommend=True):
        for _ in range(10):
            self.ensure_in_taobao()
            nodes = self.nodes()
            self.fail_if_security_verification(nodes)
            if (self.find('获取短信验证码', nodes=nodes) is not None or
                    self.find('支付宝登录', contains=True, nodes=nodes) is not None):
                self.edge_back(wait=2)
                continue
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                if select_recommend:
                    recommend = self.find('推荐', contains=True, max_y=120)
                    if recommend is not None:
                        self.tap_node(recommend)
                        time.sleep(3)
                return
            self.edge_back(wait=2)
        self.fail('多次返回后仍未到达淘宝主界面')

    def select_home_channel(self, name):
        self.tap(name, contains=True, max_y=120, wait=4)

    def select_third_home_channel(self):
        """按 Excel 的“第三个 tab”选择；当前版本该频道名为“闪购”。"""
        tabs = []
        for node in self.nodes():
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and 45 <= float(node.get('y', 0)) <= 100
                    and float(node.get('width', 0)) >= 40
                    and ('已选中' in self.node_name(node)
                         or '未选中' in self.node_name(node))):
                tabs.append(node)
        tabs.sort(key=lambda node: float(node.get('x', 0)))
        if len(tabs) < 3:
            self.fail('淘宝首页顶部不足3个频道，无法执行“第三个tab”')
        logging.info('第三个首页频道为：%s', self.node_name(tabs[2]))
        self.tap_node(tabs[2])
        time.sleep(4)

    def open_search(self):
        self.tap('搜索栏', max_y=170, wait=3)
        self.fail_if_security_verification()
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeSearchField',
                                   'XCUIElementTypeTextField')]
        if not fields:
            self.fail('点击搜索栏后未进入淘宝搜索页')

    def search(self, keyword):
        self.enter_text(keyword, clear=True)
        # 键盘弹出动画期间搜索按钮偶尔短暂不在 source 中；坐标由
        # 2026-09-16 weditor（402 x 874）核对。
        self.tap('搜索', max_y=150, fallback=(348, 86),
                 timeout=10, wait=7)
        self.fail_if_security_verification()

    def sort_by_sales(self):
        self.tap('销量', contains=True, max_y=520, wait=4)
        self.fail_if_security_verification()

    def open_first_product(self):
        nodes = self.nodes()
        products = self.matching_nodes(
            '商品图片', min_y=150, max_y=760, nodes=nodes)
        if products:
            self.tap_node(products[0])
        else:
            cards = []
            for node in nodes:
                y = float(node.get('y', 0))
                width = float(node.get('width', 0))
                height = float(node.get('height', 0))
                if (node.get('visible') == 'true'
                        and node.tag == 'XCUIElementTypeOther'
                        and 140 <= y < 760 and width >= 150 and height >= 100):
                    cards.append(node)
            if cards:
                cards.sort(key=lambda node: (
                    float(node.get('y', 0)), float(node.get('x', 0))))
                self.tap_node(cards[0])
            else:
                # 销量筛选后的商品瀑布流由画布绘制，当前版本不暴露商品卡片。
                # 2026-09-16 weditor（402 x 874）首件商品图片中心约为
                # (100, 600)，与旧脚本的首商品坐标一致。
                logging.warning('商品卡片未暴露给 WDA，使用 weditor 核对坐标')
                self.device.click(100, 600)
        time.sleep(7)
        self.wait_product_detail()

    def wait_product_detail(self, timeout=12):
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            if (self.find('客服', min_y=700, nodes=nodes) is not None or
                    self.find('加入购物车', contains=True,
                              min_y=650, nodes=nodes) is not None):
                return
            self.fail_if_security_verification(nodes)
            if time.monotonic() >= deadline:
                self.fail('未进入淘宝商品详情页')
            time.sleep(0.5)

    def open_reviews(self):
        # 淘宝 10.66.0 商品页顶部固定提供“评价”Tab，作用等同 Excel
        # 中的“查看更多查看宝贝评价”，且比详情流中的动态入口稳定。
        top_review = self.find('评价', max_y=160)
        if top_review is not None:
            self.tap_node(top_review)
            time.sleep(5)
            return
        for _ in range(8):
            nodes = self.nodes()
            review = self.find('查看更多', '查看全部评价', '宝贝评价',
                               contains=True, min_y=100, max_y=760,
                               nodes=nodes)
            if review is not None:
                self.tap_node(review)
                time.sleep(5)
                return
            self.device.swipe(0.5, 0.75, 0.5, 0.32, 0.3)
            time.sleep(1)
        self.fail('商品详情中未找到“查看更多/宝贝评价”入口')

    def return_product_detail(self):
        product_tab = self.find('宝贝', max_y=160)
        if product_tab is not None:
            self.tap_node(product_tab)
            time.sleep(5)
            self.wait_product_detail()
            return
        self.edge_back(wait=5)
        self.wait_product_detail()

    def open_customer_service(self):
        self.tap('客服', contains=True, min_y=650, wait=6)
        self.ensure_in_taobao()
        self.fail_if_login_required()
        self.fail_if_chat_login_required()

    def send_text_message(self, text):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeTextField',
                                   'XCUIElementTypeTextView')
                  and float(node.get('y', 0)) > 400]
        if fields:
            self.tap_node(fields[-1])
        else:
            logging.warning('客服输入框未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(151, 808)
        time.sleep(1)
        self.enter_text(text, clear=False)
        self.tap('发给客服', '发送', contains=True, min_y=600, wait=4)

    def send_first_photo(self):
        plus = self.find('加号面板', '+', '更多', '添加',
                         contains=True, min_y=400)
        if plus is not None:
            self.tap_node(plus)
        else:
            self.device.click(372, 511)
        time.sleep(3)
        self.tap('相册', '照片', contains=True, fallback=(150, 602), wait=5)

        nodes = self.nodes()
        if (self.find('允许访问所有照片', contains=True, nodes=nodes)
                is not None or self.find('选择照片', nodes=nodes) is not None):
            self.fail('淘宝尚未获得照片权限，请先人工授权照片访问')

        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and (self.node_name(node).startswith('未选中 照片')
                           or self.node_name(node).startswith('未选中 图片')
                           or self.node_name(node) == 'icon_checkbox_unselect')]
        candidates.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        if candidates:
            self.tap_node(candidates[0])
        else:
            logging.warning('相册缩略图未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(88, 150)
        time.sleep(2)
        self.tap('发送 (1)', '发送(1)', '发送（1）', '发送',
                 contains=True, fallback=(347, 815), min_y=650, wait=6)

    def enter_store(self):
        self.tap('店铺', '进店', '进入店铺', contains=True,
                 fallback=(27, 809), min_y=650, wait=7)
        nodes = self.nodes()
        store_home = self.find('首页', contains=True, min_y=760, nodes=nodes)
        store_goods = self.find('宝贝', '全部商品', '商品分类', '分类',
                                contains=True, min_y=700, nodes=nodes)
        if store_home is None or store_goods is None:
            self.fail('点击店铺图标后未进入店铺页面')

    def browse_store(self):
        # Excel 语序有歧义。按旧脚本意图处理为：点店铺图标进入后，
        # 先上滑一次，再上滑3次、下滑3次。
        self.device.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
        time.sleep(1)
        self.browse(3, 3)

    def add_to_cart(self):
        self.tap('加入购物车', contains=True, min_y=650, wait=4)
        nodes = self.nodes()
        if self.find('请选择', contains=True, nodes=nodes) is not None:
            self.fail('商品需要选择规格；请预先选择默认规格或更换免选规格商品')
        confirm = self.find('加入购物车', contains=True, min_y=650,
                            nodes=nodes)
        if confirm is not None:
            self.tap_node(confirm)
            time.sleep(4)

    def open_bottom_tab(self, *names):
        self.tap(*names, min_y=760, wait=5)

    def open_guangguang(self):
        # 淘宝 10.66.0 已将底栏“逛逛”改名为“视频”。
        self.open_bottom_tab('逛逛', '视频')

    def horizontal_browse(self, right, left):
        for _ in range(right):
            self.device.swipe(0.25, 0.5, 0.75, 0.5, 0.3)
            time.sleep(1)
        for _ in range(left):
            self.device.swipe(0.75, 0.5, 0.25, 0.5, 0.3)
            time.sleep(1)
        time.sleep(1)

    def open_my_taobao(self):
        self.open_bottom_tab('我的淘宝')
        self.ensure_in_taobao()
        self.fail_if_login_required()

    def open_my_orders(self):
        self.tap('我的订单', contains=True, max_y=500, wait=6)
        self.ensure_in_taobao()
        self.fail_if_login_required()
