import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_fanqiechangting_0010(WdaCase):
    """Excel 7.0.2：搜索、短剧和音乐频道浏览。"""

    PACKAGE = 'com.xs.fm'
    APP_NAME = '番茄畅听'

    def prepare_iteration(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        self.device.app_terminate(self.PACKAGE)
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

    def start_changting(self):
        self.start_app(wait=5)
        for _ in range(3):
            nodes = self.nodes()
            prompt = self.find('以后再说', '不允许', '暂不', nodes=nodes)
            if prompt is None:
                break
            self.tap_node(prompt)
            time.sleep(1)
        self.tap('首页', min_y=760, wait=2)
        self.tap('推荐', max_y=170, wait=2)

    def search_olympics(self):
        # 2026-09-12 weditor（402×874）：首页顶部搜索框文案动态变化。
        self.device.click(190, 84)
        time.sleep(3)
        self.wait_for('搜索', max_y=130, timeout=8)
        self.enter_text('奥运会', clear=True)
        self.tap('搜索', max_y=130, wait=5)

    def return_home(self):
        self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(3)
        self.wait_for('首页', min_y=760, timeout=8)

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动番茄畅听')
                self.start_changting()
            self.step(2, '首页滑动，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击上方搜索框，输入奥运会，点击搜索')
            self.search_olympics()
            self.step(4, '在搜索界面，上滑5次')
            self.browse(5, 0)
            self.step(5, '侧滑返回到首页')
            self.return_home()
            self.step(6, '点击短剧，进入短剧推荐页面')
            self.tap('短剧', max_y=180, wait=4)
            self.step(7, '短剧推荐页面滑动，上滑10次')
            self.browse(10, 0)
            self.step(8, '点击底部首页')
            self.tap('首页', min_y=760, wait=3)
            self.tap('推荐', max_y=180, wait=2)
            self.step(9, '首页上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(10, '点击音乐')
            self.tap('音乐', max_y=180, wait=4)
            with self.capture_trace(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
