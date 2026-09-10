"""高德地图动态性能用例的 iOS WDA 公共操作。"""

import logging
import os
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager

from aw import SeaOfStarsAW
from cases.CaseBase import Case


class AutonaviCase(Case):
    PACKAGE = 'com.autonavi.amap'
    XHS_PACKAGE = 'com.xingin.discover'
    DOUYIN_PACKAGE = 'com.ss.iphone.ugc.Aweme'
    all_app_package_list = [PACKAGE]
    TEST_TIME = 1
    STEP_INTERVAL = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__
        self.current_step = '准备环境'
        self._has_step = False
        self._trace_active = False

    @property
    def device(self):
        return SeaOfStarsAW.ut_device

    @contextmanager
    def capture_trace(self, iteration, step_number):
        """只包围首尾单步；每轮固定生成两份短 trace。"""
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        if step_number == 1:
            self._has_step = False
        try:
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'round_{}_step_{}'.format(iteration + 1, step_number),
                self.screenshot_dir_path,
            )
            self._trace_active = True
            yield
        finally:
            self._trace_active = False
            SeaOfStarsAW.stop_trace()

    @SeaOfStarsAW.function_log
    def set_up(self):
        missing = [package for package in self.all_app_package_list
                   if self.device.app_state(package)['value'] == 0]
        if missing:
            raise RuntimeError('设备未安装应用：{}'.format(', '.join(missing)))
        return True

    def step(self, number, text):
        if self._has_step:
            time.sleep(self.STEP_INTERVAL)
        self._has_step = True
        self.current_step = '{}、{}'.format(number, text)
        logging.info(self.current_step)
        if self._trace_active and SeaOfStarsAW.trace_thread is not None:
            SeaOfStarsAW.trace_thread.add_log('高德地图', self.current_step)

    def fail(self, message):
        path = os.path.join(
            self.screenshot_dir_path,
            'step_{}_failed.png'.format(self.current_step.split('、')[0]),
        )
        try:
            self.device.screenshot(path)
        except Exception:
            logging.exception('失败截图保存失败')
        raise AssertionError('{}：{}'.format(self.current_step, message))

    def nodes(self):
        # 高德页面切换时偶发返回一次空 source，短暂重试避免误判页面状态。
        last_error = None
        for _ in range(4):
            try:
                source = self.device.source()
                if source and source.strip():
                    return list(ET.fromstring(source).iter())
            except Exception as error:
                # 退出导航或重启高德时 USB WDA 连接可能短暂重建。
                last_error = error
                logging.warning('读取 WDA 页面层级失败，正在重试：%s', error)
            time.sleep(1)
        if last_error is not None:
            self.fail('WDA 页面层级读取失败：{}'.format(last_error))
        self.fail('WDA 未返回页面层级')

    @staticmethod
    def node_name(node):
        return node.get('name') or node.get('label') or node.get('value') or ''

    def matching_nodes(self, *names, min_y=None, max_y=None, contains=False, nodes=None):
        result = []
        for node in self.nodes() if nodes is None else nodes:
            if node.get('visible') != 'true' or node.get('enabled') == 'false':
                continue
            name = self.node_name(node)
            if not name:
                continue
            y = float(node.get('y', 0))
            if min_y is not None and y < min_y:
                continue
            if max_y is not None and y > max_y:
                continue
            matched = any(candidate == name for candidate in names)
            if contains:
                matched = matched or any(candidate in name for candidate in names)
            if matched:
                result.append(node)
        return sorted(result, key=lambda n: (float(n.get('y', 0)), float(n.get('x', 0))))

    def find(self, *names, **kwargs):
        matches = self.matching_nodes(*names, **kwargs)
        return matches[0] if matches else None

    def tap_node(self, node):
        x, y, width, height = (float(node.get(k, 0)) for k in ('x', 'y', 'width', 'height'))
        if width <= 0 or height <= 0:
            self.fail('控件没有可点击区域：{}'.format(self.node_name(node)))
        # 出行方式横向栏会把“驾车”部分移出屏幕；点击可见区域中心，避免负坐标失效。
        window_width, window_height = self.device.window_size()
        left, right = max(0, x), min(window_width, x + width)
        top, bottom = max(0, y), min(window_height, y + height)
        if right <= left or bottom <= top:
            self.fail('控件位于屏幕外：{}'.format(self.node_name(node)))
        self.device.click(round((left + right) / 2), round((top + bottom) / 2))

    def tap(self, *names, fallback=None, wait=2, timeout=6, min_y=None,
            max_y=None, contains=False, choose='first'):
        deadline = time.monotonic() + timeout
        while True:
            matches = self.matching_nodes(
                *names, min_y=min_y, max_y=max_y, contains=contains)
            if matches:
                self.tap_node(matches[-1] if choose == 'last' else matches[0])
                break
            if time.monotonic() >= deadline:
                if fallback is None:
                    self.fail('未找到控件：{}'.format(' / '.join(names)))
                logging.warning('控件 %s 不可访问，使用 weditor 核对坐标 %s', names, fallback)
                self.device.click(*fallback)
                break
            time.sleep(0.5)
        time.sleep(max(self.STEP_INTERVAL, wait))

    def browse(self, up, down, wait=1):
        for start, end, count in ((0.75, 0.35, up), (0.35, 0.75, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(wait)
        time.sleep(1)

    def launcher(self):
        for _ in range(2):
            self.device.swipe(0.5, 0.995, 0.5, 0.15, 0.1)
            time.sleep(2)
            if self.device.app_current().get('bundleId') == 'com.apple.springboard':
                return
        self.fail('滑动后未回到 Home 页')

    def start_app(self, package, wait=4):
        last_error = None
        for _ in range(5):
            try:
                if self.device.locked():
                    self.device.unlock()
                    time.sleep(2)
                self.device.app_activate(package)
                last_error = None
                break
            except Exception as error:
                last_error = error
                logging.warning('WDA 连接暂不可用，重试启动%s：%s', package, error)
                time.sleep(2)
        if last_error is not None:
            self.fail('WDA 无法启动应用：{}'.format(last_error))
        time.sleep(wait)

    def start_autonavi(self):
        self.start_app(self.PACKAGE, wait=4)
        # 普通用例要从可确认的高德首页开始。
        self.return_autonavi_home()

    def resume_navigation(self):
        """恢复被放入后台的高德导航，不做首页重置。"""
        self.start_app(self.PACKAGE, wait=4)
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            nodes = self.nodes()
            if self.in_navigation(nodes):
                return
            time.sleep(1)
        self.fail('未恢复到后台导航页，请先成功执行 0070')

    def open_search(self):
        # 26.6.1 实机上文案会根据历史地点变化，weditor 稳定前缀是
        # “搜索框，输入文字”。不再使用坐标兜底，避免非首页时误点地图。
        self.tap('搜索框，输入文字', wait=2, timeout=10, contains=True)

    def enter_search_text(self, text):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag.endswith('TextField')]
        if fields:
            field = self.device(type='XCUIElementTypeTextField', visible=True)
            field.clear_text()
            field.set_text(text)
        else:
            # 高德首次进入搜索页时输入框不在 WDA 树中，但键盘已获得焦点。
            self.device.send_keys(text)
        time.sleep(3)

    def search(self, text):
        self.open_search()
        self.enter_search_text(text)

    def tap_first_route(self):
        # weditor 实测：输入“西安北站”后首条建议的右侧会暴露“路线”。
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            matches = self.matching_nodes('路线', min_y=120, max_y=760)
            if matches:
                self.tap_node(matches[0])
                time.sleep(4)
                return
            time.sleep(0.5)
        self.fail('搜索结果中未找到第一条路线入口')

    def select_driving(self):
        nodes = self.nodes()
        driving_nodes = self.matching_nodes('驾车', contains=True, max_y=220, nodes=nodes)
        selected = next((item for item in driving_nodes
                         if '已选中' in self.node_name(item)), None)
        if selected is not None:
            return
        node = driving_nodes[0] if driving_nodes else None
        if node is None:
            self.fail('路线页未找到驾车出行方式')
        self.tap_node(node)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            nodes = self.nodes()
            if self.find('开始导航', contains=True, nodes=nodes) is not None:
                driving = self.find('驾车', contains=True, max_y=220, nodes=nodes)
                if driving is None or '已选中' in self.node_name(driving):
                    return
            time.sleep(1)
        self.fail('点击驾车后未切换到驾车路线页')

    def in_navigation(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        names = [self.node_name(node) for node in nodes if node.get('visible') == 'true']
        if any(name == '退出导航按钮' for name in names):
            return True
        # 步行导航页没有“退出导航按钮”，以转向提示和到达时间共同判定。
        return (any('米后' in name for name in names)
                and any(name == '到达' or name.endswith('到达') for name in names))

    def accept_navigation_notice(self, nodes):
        consent = self.find('同意', nodes=nodes)
        title = self.find('导航使用提示', contains=True, nodes=nodes)
        if consent is None or title is None:
            return False
        logging.info('处理一次性提示：%s', self.node_name(title))
        self.tap_node(consent)
        time.sleep(4)
        return True

    def start_navigation(self):
        self.tap('开始导航', fallback=(0.75, 0.94), wait=2, timeout=10, contains=True)
        deadline = time.monotonic() + 20
        clicked_again = False
        while time.monotonic() < deadline:
            nodes = self.nodes()
            if self.in_navigation(nodes):
                return
            if self.accept_navigation_notice(nodes):
                continue
            # 路线刚刷新时首次点击可能被吞掉；仍在路线页时只补点一次。
            start = self.find('开始导航', contains=True, nodes=nodes)
            if start is not None and not clicked_again:
                self.tap_node(start)
                clicked_again = True
            time.sleep(1)
        self.fail('点击开始导航后未进入导航页')

    def open_exit_navigation(self):
        nodes = self.nodes()
        node = self.find('退出导航按钮', nodes=nodes)
        if node is not None:
            self.tap_node(node)
        elif self.in_navigation(nodes):
            # 步行导航的退出入口是左下角无障碍未命名的“×”。
            self.device.click(0.2, 0.905)
        else:
            self.device.click(0.11, 0.93)
        time.sleep(2)

    def confirm_exit_navigation(self):
        for name in ('退出导航', '确认退出', '结束导航'):
            node = self.find(name, contains=True)
            if node is not None and self.node_name(node) != '退出导航按钮':
                self.tap_node(node)
                time.sleep(4)
                return
        # 26.6.1 实测导航页偶发不展示确认层；重启高德可安全结束后台导航并回地图页。
        logging.warning('退出确认控件未暴露，重启高德结束导航')
        self.device.app_terminate(self.PACKAGE)
        time.sleep(1)
        self.device.app_activate(self.PACKAGE)
        time.sleep(4)

    def return_autonavi_home(self):
        restarted = False
        for _ in range(10):
            nodes = self.nodes()
            # 不能只看到“首页”Tab就返回；打车/我的等页面也有该 Tab。
            # 必须同时看到主地图的动态搜索框才算真正回到首页。
            search_box = self.find('搜索框，输入文字', contains=True, nodes=nodes)
            tab_bar = self.find('标签页栏', nodes=nodes)
            if search_box is not None and tab_bar is not None:
                return

            if self.in_navigation(nodes):
                self.open_exit_navigation()
                self.confirm_exit_navigation()
                continue

            home_nodes = self.matching_nodes('首页', min_y=760, nodes=nodes)
            if home_nodes:
                self.tap_node(home_nodes[0])
                time.sleep(3)
                continue

            node = self.find('返回', '关闭', '取消', nodes=nodes)
            if node is not None:
                self.tap_node(node)
                time.sleep(3)
                continue

            # 原先的无条件侧滑会在沉浸式地图上变成“平移地图”，最终
            # 永远回不到首页。遇到无可用导航控件的页面时重启一次应用。
            if not restarted:
                logging.warning('当前高德页面无可用返回控件，重启应用后继续恢复首页')
                self.device.app_terminate(self.PACKAGE)
                time.sleep(1)
                self.device.app_activate(self.PACKAGE)
                restarted = True
            else:
                # 重启后若是可点击的全屏地图，单击一次恢复顶/底部控件。
                self.device.click(0.5, 0.5)
            time.sleep(4)
        self.fail('未返回高德地图主界面')

    def pinch_map(self):
        window = self.device(type='XCUIElementTypeWindow').get(timeout=5)
        window.pinch(2.0, 1.0)
        time.sleep(2)
        window.pinch(0.5, -1.0)
        time.sleep(2)

    def open_taxi_tab(self):
        self.tap('打车', min_y=760, choose='last', fallback=(0.67, 0.94), wait=4)

    def open_first_result(self):
        # 搜索结果首卡的标题随位置变化，weditor 实测卡片中心稳定。
        self.device.click(0.5, 0.34)
        time.sleep(4)

    def open_first_transit_route(self):
        # 公交/飞机组合方案卡未暴露统一控件名，点击首个方案正文。
        self.device.click(0.5, 0.36)
        time.sleep(3)
