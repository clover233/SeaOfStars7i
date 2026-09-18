"""闲鱼动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class XianyuCase(WdaCase):
    PACKAGE = 'com.taobao.fleamarket'
    APP_NAME = '闲鱼'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        self._previous_idle_settings = None
        try:
            settings = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': settings.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': settings.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置闲鱼 WDA 连续页面模式失败')
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束闲鱼进程失败，继续启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            settings = getattr(self, '_previous_idle_settings', None)
            if settings is not None:
                try:
                    self.device.appium_settings(settings)
                except Exception:
                    logging.exception('恢复 WDA idle 设置失败')
            self._previous_idle_settings = None

    def dismiss_startup_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            button = self.find(
                '同意并继续', '同意', '允许', '使用App时允许',
                '要求 App 不跟踪', '暂不更新', '以后再说',
                '我知道了', '跳过', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def edge_back(self, wait=2):
        back = self.find('返回', '返回按钮', contains=True, max_y=150)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(4, 437, 350, 437, 0.3)
        time.sleep(wait)

    def return_xianyu_home(self):
        for _ in range(9):
            nodes = self.nodes()
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(3)
                if self.find('推荐', max_y=230) is not None:
                    return
                continue
            if self.find('分享至', contains=True, nodes=nodes) is not None:
                self.device.click(201, 830)
                time.sleep(2)
                continue
            self.edge_back(wait=2)
        self.fail('多次返回后仍未到达闲鱼首页')

    def start_xianyu(self):
        self.start_app(wait=0)

    def finish_xianyu_start(self):
        self.dismiss_startup_prompts()
        self.return_xianyu_home()

    def open_search(self):
        search = self.find('搜索', max_y=170)
        if search is not None:
            self.tap_node(search)
        else:
            # 2026-09-18 WEditor，402x874：首页搜索图标中心。
            logging.warning('闲鱼搜索图标未暴露，使用 WEditor 核对坐标')
            self.device.click(369, 130)
        time.sleep(3)

    def search(self, query):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeTextField']
        if not fields:
            self.device.click(90, 84)
            time.sleep(2)
        self.enter_text(query, clear=True)
        self.tap('Search', '搜索', min_y=700, wait=6)

    def open_first_product(self):
        candidates = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeStaticText'
                      and 390 <= float(node.get('y', 0)) <= 760
                      and float(node.get('width', 0)) >= 150
                      and len(self.node_name(node)) >= 15]
        if not candidates:
            self.fail('搜索结果中没有可打开的商品')
        candidates.sort(key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(candidates[0])
        time.sleep(6)
        if self.find('分享按钮', max_y=150) is None:
            self.fail('点击第一个商品后未进入详情页')

    def open_and_close_share(self):
        self.tap('分享按钮', max_y=150, wait=4)
        # 当前分享面板整体为 Canvas，“取消”未单独暴露。
        self.device.click(201, 830)
        time.sleep(3)
        if self.find('分享按钮', max_y=150) is None:
            self.fail('关闭分享面板后未返回商品详情页')
