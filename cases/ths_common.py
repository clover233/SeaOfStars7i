"""同花顺动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class ThsCase(WdaCase):
    PACKAGE = 'cn.com.10jqka.IHexin'
    APP_NAME = '同花顺'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只在首尾步骤采集，并保证采样窗口不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
        """行情和分时图持续刷新时不等待 XCTest 进入 idle。"""
        self._previous_idle_settings = None
        try:
            current = self.device.appium_settings()
            self._previous_idle_settings = {
                'waitForIdleTimeout': current.get('waitForIdleTimeout', 10),
                'animationCoolOffTimeout': current.get(
                    'animationCoolOffTimeout', 2),
            }
            self.device.appium_settings(
                {'waitForIdleTimeout': 0, 'animationCoolOffTimeout': 0})
        except Exception:
            logging.exception('设置 WDA 连续页面模式失败')

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is not None:
            try:
                self.device.appium_settings(previous)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束同花顺进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def fail_if_manual_confirmation_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('同意并继续', nodes=nodes) is not None or
                self.find('隐私政策', contains=True, nodes=nodes) is not None):
            self.fail('同花顺尚未确认隐私协议，请先人工确认后再运行')
        if (self.find('风险提示', contains=True, nodes=nodes) is not None and
                self.find('我已阅读', contains=True, nodes=nodes) is not None):
            self.fail('同花顺显示风险提示，请先人工阅读并确认后再运行')

    def dismiss_optional_prompts(self):
        """关闭普通权限、更新、引导和广告弹窗。"""
        for _ in range(6):
            nodes = self.nodes()
            self.fail_if_manual_confirmation_required(nodes)
            button = self.find(
                '不允许', '要求App不跟踪', '要求 App 不跟踪',
                '以后再说', '下次再说', '暂不开启', '暂不升级',
                '我知道了', '取消', '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=180, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_ths(self):
        self.start_app(wait=5)
        self.dismiss_optional_prompts()
        self.return_home()

    def edge_back(self, wait=3):
        back = self.find('返回', contains=True, max_y=150)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                landed = self.nodes()
                if (self.find('tab_shouye_selected', nodes=landed) is not None
                        or self.find('搜索', max_y=130, nodes=landed) is not None):
                    return
            else:
                self.edge_back(wait=3)
        self.fail('多次返回后仍未到达同花顺主界面')

    def open_watchlist(self):
        self.tap('自选', min_y=760, wait=5)
        nodes = self.nodes()
        if (self.find('同花顺自选', max_y=150, nodes=nodes) is None or
                self.find('自选股', max_y=260, nodes=nodes) is None):
            self.fail('点击“自选”后未进入自选股页面')
        if self.find('暂无自选', contains=True, nodes=nodes) is not None:
            self.fail('自选股列表为空，请预先添加足够股票后再运行')

    def open_stock_search(self):
        self.tap('搜索', max_y=150, wait=3)
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeTextField'
                  and self.node_name(node) == 'searchBar']
        if not fields:
            self.fail('点击搜索按钮后未进入股票搜索页')

    def input_stock_keyword(self, keyword):
        self.enter_text(keyword, clear=True)
        deadline = time.monotonic() + 8
        while True:
            if self.find(keyword, min_y=90, max_y=260) is not None:
                return
            if time.monotonic() >= deadline:
                self.fail('输入“{}”后未出现股票联想结果'.format(keyword))
            time.sleep(0.5)

    def open_stock_result(self, stock_name):
        self.tap(stock_name, min_y=90, max_y=260, wait=6)
        nodes = self.nodes()
        if (self.find(stock_name, max_y=150, nodes=nodes) is None or
                self.find('加自选', '删自选', min_y=700, nodes=nodes) is None):
            self.fail('点击“{}”后未进入股票详情页'.format(stock_name))

    def add_current_stock(self):
        nodes = self.nodes()
        if self.find('删自选', min_y=700, nodes=nodes) is not None:
            self.fail('格力电器已经在自选列表中，请先删除后再运行')
        self.tap('加自选', min_y=700, wait=4)
        if self.find('删自选', min_y=700) is None:
            self.fail('点击“加自选”后按钮未切换为“删自选”')

    def remove_current_stock(self):
        self.tap('删自选', min_y=700, wait=4)
        if self.find('加自选', min_y=700) is None:
            self.fail('点击“删自选”后按钮未切换为“加自选”')
