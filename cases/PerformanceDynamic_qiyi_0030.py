"""爱奇艺搜索播放动态性能用例。"""

import logging
import time

from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_qiyi_0030(WdaCase):
    """Excel 7.0.2：频道浏览，重复搜索并播放《大话天仙》。"""

    PACKAGE = 'com.qiyi.iphone'
    APP_NAME = '爱奇艺'

    def enable_continuous_ui_mode(self):
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

    def restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is None:
            return
        try:
            self.device.appium_settings(previous)
        except Exception:
            logging.exception('恢复 WDA idle 等待设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self.enable_continuous_ui_mode()
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

    def dismiss_optional_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            prompt = self.find(
                '同意并继续', '不允许', '以后再说', '暂不', '我知道了',
                '关闭', '跳过', nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(1)

    def edge_back(self):
        self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(2)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self.restore_idle_settings()

    def return_home(self):
        for _ in range(8):
            nodes = self.nodes()
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                return
            back = self.find(
                'pread mini back iphone', 'title back',
                max_y=130, nodes=nodes)
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            else:
                self.edge_back()
        self.fail('多次返回后仍未到达爱奇艺主界面')

    def start_qiyi(self):
        self.start_app(wait=6)
        self.dismiss_optional_prompts()
        self.return_home()

    def open_search(self):
        self.return_home()
        self.tap('进入搜索', max_y=130, wait=4)
        self.wait_for('搜索', max_y=150, timeout=10)

    def input_keyword(self, keyword):
        # 当前搜索首页的输入框由自绘视图承载，键盘已聚焦时直接输入最稳定。
        self.enter_text(keyword, clear=True)

    def submit_search(self):
        self.tap('搜索', max_y=130, wait=6, choose='last')
        self.wait_for('立即播放', '继续播放', timeout=15)

    def repeat_search(self, keyword):
        self.submit_search()
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeTextField']
        if not fields:
            self.fail('搜索结果页未找到搜索输入框')
        self.tap_node(fields[-1])
        time.sleep(2)
        self.enter_text(keyword, clear=True)
        self.submit_search()

    def return_recommendation_and_search(self):
        self.return_home()
        # 频道栏会保留在“电影”附近；向右滑回首屏后再选推荐首页。
        for _ in range(4):
            nodes = self.nodes()
            home = self.find('首页', max_y=170, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                break
            self.device.swipe(0.25, 0.135, 0.82, 0.135, 0.3)
            time.sleep(1)
        else:
            self.fail('频道栏中未找到首页')
        self.tap('进入搜索', max_y=130, wait=4)
        self.wait_for('搜索', max_y=150, timeout=10)

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动爱奇艺')
                self.start_qiyi()
            self.step(2, '首页浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击电视剧tab页')
            self.tap('电视剧', max_y=170, wait=4)
            self.step(4, '电视剧tab页浏览上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(5, '点击电影tab页')
            self.tap('电影', max_y=170, wait=4)
            self.step(6, '电影tab页浏览上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(7, '返回推荐页点击搜索框，切换到搜索页面')
            self.return_recommendation_and_search()
            self.step(8, '输入大话天仙')
            self.input_keyword('大话天仙')
            self.step(9, '搜索视频大话天仙，重复搜索2次')
            self.repeat_search('大话天仙')
            self.step(10, '点击播放大话天仙，观看30秒')
            self.tap('立即播放', '继续播放', wait=5)
            time.sleep(30)
            self.step(11, '视频播放页浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(12, '返回爱奇艺主界面')
            self.return_home()
            with self.capture_trace(iteration, 13):
                self.step(13, '上滑返回桌面')
                self.launcher()
                time.sleep(5)
