import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_pinduoduo_0010(WdaCase):
    """Excel 7.0.2：搜索华为手机，浏览商品和店铺。"""

    PACKAGE = 'com.xunmeng.pinduoduo'
    APP_NAME = '拼多多'

    def check_account_blocker(self):
        nodes = self.nodes()
        if (self.find('实名认证提示', nodes=nodes) is not None
                or self.find('提交实名信息', nodes=nodes) is not None):
            self.fail('账号被实名认证提示拦截；请先完成实名或更换不受限账号')

    def first_product(self):
        # 回到搜索结果顶部，保证选择的是第一件商品。
        self.device.click(0.5, 0.02)
        time.sleep(2)
        candidates = []
        for node in self.nodes():
            if node.tag != 'XCUIElementTypeImage' or node.get('visible') != 'true':
                continue
            y = float(node.get('y', 0))
            width = float(node.get('width', 0))
            height = float(node.get('height', 0))
            if 160 <= y <= 700 and width >= 100 and height >= 100:
                candidates.append(node)
        if not candidates:
            self.fail('搜索结果页没有可点击的商品')
        return sorted(candidates, key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))[0]

    def return_to_pdd_home(self):
        for _ in range(5):
            nodes = self.nodes()
            if self.find('已选中首页', nodes=nodes) is not None:
                return
            back = self.find('返回', 'Back', nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.9, 0.5, 0.3)
            time.sleep(3)
        self.fail('未能返回拼多多主界面')

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.device.app_terminate(self.PACKAGE)
            time.sleep(1)
            with self.capture_trace(iteration, 1):
                self.step(1, '启动拼多多')
                self.start_app(wait=5)

            self.step(2, '拼多多首页上滑3次，下滑3次')
            self.browse(3, 3)

            self.step(3, '点击上方搜索框')
            self.tap('搜索', fallback=(0.5, 0.085), wait=2)

            self.step(4, '输入华为手机，点击搜索')
            self.enter_text('华为手机', clear=True)
            self.tap('搜索', wait=6, choose='last')

            self.step(5, '搜索结果页上滑3次，下滑3次')
            self.browse(3, 3)

            self.step(6, '点击第一个商品')
            self.tap_node(self.first_product())
            time.sleep(7)
            self.check_account_blocker()

            self.step(7, '商品详情页上滑2次，下滑2次')
            self.browse(2, 2)

            self.step(8, '点击左下角店铺')
            self.tap('店铺', '进店逛逛', fallback=(0.08, 0.94), wait=6)

            self.step(9, '店铺页上滑2次，下滑2次')
            self.browse(2, 2)

            self.step(10, '返回拼多多主界面')
            self.return_to_pdd_home()

            with self.capture_trace(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
