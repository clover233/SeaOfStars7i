"""铁路 12306 动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class Tielu12306Case(WdaCase):
    PACKAGE = 'cn.12306.rails12306'
    APP_NAME = '铁路12306'

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
        """首页轮播和 H5 页持续刷新时不等待 XCTest 进入 idle。"""
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
            logging.exception('设置铁路12306连续页面模式失败')

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
            logging.exception('结束铁路12306进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def fail_if_manual_confirmation_required(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if (self.find('同意并继续', nodes=nodes) is not None or
                self.find('服务协议及隐私权政策', contains=True,
                          nodes=nodes) is not None):
            self.fail('铁路12306尚未确认隐私协议，请先人工确认后再运行')

    def dismiss_optional_prompts(self):
        """关闭非必要权限、更新、引导和普通运营弹窗。"""
        for _ in range(6):
            nodes = self.nodes()
            self.fail_if_manual_confirmation_required(nodes)
            button = self.find(
                '不允许', '要求App不跟踪', '要求 App 不跟踪',
                '以后再说', '下次再说', '暂不开启', '暂不更新',
                '我知道了', '取消', '稍后', '跳过', '关闭', nodes=nodes)
            if button is None:
                button = self.find('跳过广告', '关闭广告', contains=True,
                                   max_y=180, nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def start_tielu12306(self):
        self.start_app(wait=6)
        self.dismiss_optional_prompts()
        self.return_home()

    def edge_back(self, wait=4):
        nodes = self.nodes()
        back = self.find('返回', max_y=150, nodes=nodes)
        if back is not None:
            self.tap_node(back)
        elif self.find('酒店', max_y=80, nodes=nodes) is not None:
            # 酒店页左上角白色返回图标未暴露 accessibility name；
            # 2026-09-16 实机 402 x 874 的图标中心为 (18, 66)。
            self.device.click(18, 66)
        else:
            self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.25)
        time.sleep(wait)

    def is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        if self.find('首页', min_y=760, nodes=nodes) is None:
            return False
        return any(node is not None for node in (
            self.find('查询车票', max_y=520, nodes=nodes),
            self.find('返回顶部', max_y=150, nodes=nodes),
            self.find('酒店住宿', nodes=nodes),
            self.find('点此可进行搜索', contains=True, max_y=150,
                      nodes=nodes),
        ))

    def return_home(self):
        for _ in range(8):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self.is_home(nodes):
                return
            home = self.find('首页', min_y=760, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(4)
                if self.is_home():
                    return
                continue
            self.edge_back(wait=4)
        self.fail('多次返回后仍未到达铁路12306主界面')

    def require_ticket_query_ready(self):
        nodes = self.nodes()
        if self.find('查询车票', max_y=520, nodes=nodes) is None:
            top = self.find('返回顶部', max_y=150, nodes=nodes)
            if top is not None:
                self.tap_node(top)
                time.sleep(4)
                nodes = self.nodes()
            else:
                for _ in range(6):
                    self.device.swipe(0.5, 0.3, 0.5, 0.85, 0.3)
                    time.sleep(1)
                    nodes = self.nodes()
                    if self.find('查询车票', max_y=520,
                                 nodes=nodes) is not None:
                        break
        departure = self.find('出发站:', contains=True, max_y=360,
                              nodes=nodes)
        arrival = self.find('到达站:', contains=True, max_y=360,
                            nodes=nodes)
        date = self.find('出发日期', contains=True, max_y=380, nodes=nodes)
        if departure is None or arrival is None or date is None:
            self.fail('首页未设置完整的出发站、到达站和出发日期')
        if any(word in self.node_name(departure) + self.node_name(arrival)
               for word in ('请选择', '未选择')):
            self.fail('请预先设置有效的出发站和到达站')

    def open_ticket_results(self):
        self.require_ticket_query_ready()
        self.tap('查询车票', max_y=520, wait=2)
        deadline = time.monotonic() + 25
        while True:
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if (self.find('耗时最短', contains=True, min_y=760,
                          nodes=nodes) is not None and
                    self.find('价格最低', contains=True, min_y=760,
                              nodes=nodes) is not None):
                return
            if self.find('暂无符合条件的车次', contains=True,
                         nodes=nodes) is not None:
                self.fail('当前预置的线路或日期没有可浏览车次')
            if time.monotonic() >= deadline:
                self.fail('查询后未进入车票结果页，请检查线路、日期和网络')
            time.sleep(0.5)

    def select_result_sort(self, *names):
        self.tap(*names, contains=True, min_y=760, timeout=10, wait=3)

    def open_hotel(self):
        """浏览后恢复到功能区，再进入酒店住宿。"""
        for _ in range(6):
            hotel = self.find('酒店住宿')
            if hotel is not None:
                self.tap_node(hotel)
                time.sleep(7)
                break
            self.device.swipe(0.5, 0.32, 0.5, 0.82, 0.3)
            time.sleep(1)
        else:
            self.fail('首页滚动后未找到“酒店住宿”入口')
        nodes = self.nodes()
        if (self.find('我的位置', contains=True, nodes=nodes) is None and
                self.find('我的订单', min_y=760, nodes=nodes) is None):
            self.fail('点击“酒店住宿”后未进入酒店页面')

    def return_from_hotel(self):
        self.edge_back(wait=5)
        if self.find('首页', min_y=760) is None:
            self.fail('从酒店页面返回后未到达铁路12306主界面')

    def open_main_tab(self, name):
        self.tap(name, min_y=760, wait=5)
        nodes = self.nodes()
        if name == '首页':
            if self.is_home(nodes):
                return
            self.fail('点击“首页”后未进入铁路12306首页')
        marker = self.find(name, max_y=150, nodes=nodes)
        if marker is None:
            self.fail('点击“{}”后未进入对应页面'.format(name))
