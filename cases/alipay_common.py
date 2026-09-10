"""支付宝 iOS 用例的定位、等待及返回操作（WDA，不使用 Android 接口）。"""

import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager

from aw import SeaOfStarsAW
from cases.CaseBase import Case


class AlipayCase(Case):
    PACKAGE = 'com.alipay.iphoneclient'
    all_app_package_list = [PACKAGE]
    TEST_TIME = 1
    STEP_INTERVAL = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__
        self.current_step = '准备环境'
        self._has_step = False
        self._trace_active = False

    @contextmanager
    def capture_trace(self, iteration, step_number):
        """仅包围首尾单步，生成两份维测短 trace；中间步骤不采集。"""
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        if step_number == 1:
            self._has_step = False
        try:
            SeaOfStarsAW.start_trace(
                self.trace_dir_path, self.__class__.__name__,
                'round_{}_step_{}'.format(iteration + 1, step_number),
                self.screenshot_dir_path)
            self._trace_active = True
            yield
        finally:
            self._trace_active = False
            SeaOfStarsAW.stop_trace()

    @property
    def device(self):
        return SeaOfStarsAW.ut_device

    @SeaOfStarsAW.function_log
    def set_up(self):
        if self.device.app_state(self.PACKAGE)['value'] == 0:
            raise RuntimeError('设备未安装支付宝')
        return True

    def step(self, number, text):
        if self._has_step:
            time.sleep(self.STEP_INTERVAL)
        self._has_step = True
        self.current_step = '{}、{}'.format(number, text)
        logging.info(self.current_step)
        if self._trace_active and SeaOfStarsAW.trace_thread is not None:
            SeaOfStarsAW.trace_thread.add_log('支付宝', self.current_step)

    def fail(self, message):
        path = os.path.join(self.screenshot_dir_path, 'step_{}_failed.png'.format(
            self.current_step.split('、')[0]))
        try:
            self.device.screenshot(path)
        except Exception:
            logging.exception('失败截图保存失败')
        raise AssertionError('{}：{}'.format(self.current_step, message))

    def nodes(self):
        return list(ET.fromstring(self.device.source()).iter())

    def find(self, *names, nodes=None):
        # 使用同一份页面快照匹配并读取坐标，避免查找后再次取 rect 时元素失效。
        for node in self.nodes() if nodes is None else nodes:
            if node.get('visible') == 'true' and node.get('enabled') != 'false':
                if node.get('name') in names or node.get('label') in names:
                    return node
                # 底部消息 tab 有未读数时，无障碍名称会附带动态计数。
                if '消息' in names and node.tag.endswith('Button') and any(
                        (node.get(key) or '').startswith('消息,未读消息')
                        for key in ('name', 'label')):
                    return node
        return None

    def require_no_alert(self, nodes=None):
        alerts = [n for n in (self.nodes() if nodes is None else nodes) if n.tag.endswith('Alert')
                  and n.get('visible') == 'true']
        if alerts:
            self.fail('请先处理系统弹窗：{}'.format(alerts[0].get('label', '未知弹窗')))

    def tap_node(self, node):
        x, y, width, height = (float(node.get(k, 0)) for k in ('x', 'y', 'width', 'height'))
        if width <= 0 or height <= 0:
            self.fail('控件没有可点击区域')
        # facebook-wda 把所有 float 都当作百分比，绝对坐标必须转 int。
        self.device.click(round(x + width / 2), round(y + height / 2))

    def tap(self, *names, fallback=None, wait=2, timeout=6):
        deadline = time.monotonic() + timeout
        while True:
            nodes = self.nodes()
            self.require_no_alert(nodes)
            node = self.find(*names, nodes=nodes)
            if node is not None:
                self.tap_node(node)
                break
            if time.monotonic() >= deadline:
                if fallback is None:
                    self.fail('未找到控件：{}'.format(' / '.join(names)))
                logging.warning('控件 %s 不可访问，使用已核对坐标 %s', names, fallback)
                self.device.click(*fallback)
                break
            time.sleep(0.5)
        time.sleep(max(self.STEP_INTERVAL, wait))

    def dismiss_popup(self):
        # 只处理可关闭的引导，不自动同意授权、开通服务或交易协议。
        node = self.find('关闭', '关闭按钮', '暂不', '以后再说', '我知道了')
        if node is not None:
            self.tap_node(node)
            time.sleep(1)

    def dismiss_finance_intro(self):
        if self.find('【定期+】【收益+】【理财+】三大系列产品') is not None:
            # weditor 2026-09-09：“金选·稳健升级”浮层底部圆形关闭按钮无名称。
            self.device.click(0.5, 0.825)
            time.sleep(1)

    def open_first_product(self):
        # 用户确认：新版没有旧版“热销”栏时，选择当前第一个推荐产品。
        # weditor：产品卡的名称位于收益率正上方；通过卡片结构选取，避免固定产品名过期。
        nodes = self.nodes()
        width, height = self.device.window_size()
        texts = [n for n in nodes if n.tag.endswith('StaticText')
                 and n.get('visible') == 'true'
                 and 0 <= float(n.get('x', 0)) < width / 2
                 and 100 < float(n.get('y', 0)) < height * 0.85]
        rates = sorted([n for n in texts if re.fullmatch(
            r'[+]\d+(?:\.\d+)?%', n.get('label') or '')], key=lambda n: float(n.get('y')))
        for rate in rates:
            x, y = float(rate.get('x')), float(rate.get('y'))
            titles = [n for n in texts if abs(float(n.get('x')) - x) < 4
                      and 15 <= y - float(n.get('y')) <= 50
                      and re.search(r'[\u4e00-\u9fff].*\d+(?:天|个月|年)', n.get('label') or '')]
            if titles:
                title = min(titles, key=lambda n: y - float(n.get('y')))
                logging.info('进入当前第一个推荐产品：%s', title.get('label'))
                self.tap_node(title)
                time.sleep(3)
                if self.find('稳健理财') is not None and self.find('市场') is not None:
                    self.fail('点击推荐产品后仍停留在稳健理财列表')
                return
        self.fail('未定位到推荐产品卡片，请使用 weditor 核对当前产品布局')

    def start_alipay(self):
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        self.device.app_activate(self.PACKAGE)
        time.sleep(3)
        self.dismiss_popup()
        self.return_tab('首页')

    def back(self):
        # 网页返回按钮经常不在 WDA 控件树中，优先命名按钮，否则侧滑。
        node = self.find('返回', '返回上一页', '返回按钮', '取消', '关闭当前小程序', '返回首页')
        if node is not None:
            self.tap_node(node)
        else:
            self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
        time.sleep(2)

    def return_tab(self, name):
        for _ in range(7):
            nodes = self.nodes()
            tabbar = next((n for n in nodes if n.tag.endswith('TabBar')
                           and n.get('visible') == 'true'
                           and any(c.get('name') == '理财' for c in n.iter())
                           and any(c.get('name') == '我的' for c in n.iter())), None)
            if tabbar is not None:
                target = self.find(name, nodes=list(tabbar.iter()))
                if target is not None:
                    self.tap_node(target)
                    time.sleep(2)
                    if name == '首页' and self.find('扫一扫') is None:
                        # 首页停留在信息流时，底部首页按钮显示“回顶部”。
                        self.tap('首页', wait=2)
                        if self.find('扫一扫') is None:
                            self.fail('首页未回到顶部，无法定位快捷入口')
                    return
            self.back()
        self.fail('返回支付宝{}页超时'.format(name))

    def return_to(self, *anchors):
        for _ in range(6):
            if self.find(*anchors) is not None:
                return
            self.back()
        self.fail('未返回目标页面：{}'.format(anchors))

    def browse(self, up, down):
        for start, end, count in ((0.75, 0.35, up), (0.35, 0.75, down)):
            for _ in range(count):
                self.device.swipe(0.5, start, 0.5, end, 0.3)
                time.sleep(1)
        time.sleep(2)

    def launcher(self):
        # 全屏页面第一次底部滑动可能只唤出 Home 指示条，允许再滑一次。
        for _ in range(2):
            self.device.swipe(0.5, 0.995, 0.5, 0.15, 0.1)
            time.sleep(2)
            if self.device.app_current().get('bundleId') == 'com.apple.springboard':
                return
        self.fail('滑动后未回到 Home 页')

    def open_chat(self, name):
        self.chat_name = name
        # 会话标题可能带未读数、时间及最后一条消息，先精确匹配，再匹配逗号前的名字。
        for _ in range(4):
            nodes = self.nodes()
            matches = [n for n in nodes if n.get('visible') == 'true'
                       and (n.get('name') == name or n.get('label') == name
                            or (n.get('label') or '').startswith(name + ','))]
            if matches:
                self.tap_node(matches[0])
                time.sleep(2)
                return
            self.device.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
            time.sleep(1)
        self.fail('消息列表中未找到聊天对象 {}'.format(name))

    def send_chat_text(self, text):
        self.require_no_alert()
        fields = [n for n in self.nodes() if n.get('visible') == 'true'
                  and n.tag in ('XCUIElementTypeTextView', 'XCUIElementTypeTextField')]
        if not fields:
            self.fail('未找到聊天输入框')
        self.tap_node(fields[-1])
        time.sleep(1)
        # 使用 WDA 的文本输入，不把 Android send_keys/description/resourceId 混入本项目。
        input_field = self.device(type=fields[-1].tag, visible=True)
        # facebook-wda 的 set_text 是追加；先清理上次失败留下的草稿。
        input_field.clear_text()
        input_field.set_text(text)
        time.sleep(1)
        for _ in range(2):
            self.tap('发送', 'Send')
            nodes = self.nodes()
            drafts = [n for n in nodes if n.tag in ('XCUIElementTypeTextView', 'XCUIElementTypeTextField')
                      and n.get('visible') == 'true' and n.get('value') == text]
            if not drafts:
                # 中文输入法首次点发送可能只提交候选词；仅在草稿还在时再点一次。
                # 草稿已清空就不重发，避免慢网络下重复发送消息。
                for _ in range(4):
                    if any(n.get('visible') == 'true' and (n.get('label') == text
                           or (n.get('label') or '').endswith('我说' + text)) for n in nodes):
                        return
                    time.sleep(1)
                    nodes = self.nodes()
                break
        self.fail('发送后聊天记录中未找到测试文本，或输入框仍有草稿')

    def photo_nodes(self):
        nodes = self.nodes()
        self.require_no_alert(nodes)
        # 扫码相册用“照片33 日期时间”等可访问名称，不能用第一个 Image（可能是图标）。
        bars = [n for n in nodes if n.tag.endswith('NavigationBar')
                and n.get('visible') == 'true']
        top = max((float(n.get('y', 0)) + float(n.get('height', 0)) for n in bars), default=100)
        photos = [n for n in nodes if n.tag.endswith('Image')
                  and n.get('visible') == 'true'
                  and re.match(r'照片\d', n.get('label') or n.get('name') or '')
                  and float(n.get('y', 0)) + float(n.get('height', 0)) > top]
        return sorted(photos, key=lambda n: (float(n.get('y', 0)), float(n.get('x', 0)))), top

    def open_chat_photos(self):
        # 聊天记录中的“图片”是已发内容；附件入口实际叫“照片”。
        node = self.find('照片')
        if node is None:
            self.tap('更多')
        self.tap('照片')

    def send_five_photos(self):
        nodes = self.nodes()
        self.require_no_alert(nodes)
        top = max((float(n.get('y', 0)) + float(n.get('height', 0)) for n in nodes
                   if n.tag.endswith('NavigationBar') and n.get('visible') == 'true'), default=100)
        if any((n.get('label') or '').startswith('已选中 照片') for n in nodes):
            self.fail('进入相册时已有选中图片，请清空选择后重新运行')
        buttons = sorted([n for n in nodes if n.tag.endswith('Button')
                          and n.get('visible') == 'true'
                          and float(n.get('y', 0)) >= top
                          and (n.get('label') or '').startswith('未选中 照片')],
                         key=lambda n: (float(n.get('y', 0)), float(n.get('x', 0))))
        if len(buttons) < 5:
            self.fail('当前相册可选择的图片不足5张，请预先准备测试图片')
        for button in buttons[:5]:
            self.tap(button.get('label'), wait=0.5)
        # 数量和完成按钮的名称在当前设备确认后匹配，不能固定点旧版相册坐标。
        nodes = self.nodes()
        selected = [n for n in nodes if n.tag.endswith('Button')
                    and n.get('visible') == 'true'
                    and (n.get('label') or '').startswith('已选中')]
        if len(selected) != 5:
            self.fail('图片选择数量不是5，实际为{}'.format(len(selected)))
        self.tap('完成', '发送', '发送(5)', '发送（5）', wait=3)
        if self.find('最近项目') is not None:
            self.fail('点击发送后仍停留在相册')
        if self.find('发送消息...') is None:
            self.fail('图片发送后没有返回聊天页')

    def preview_first_photo(self):
        photos, top = self.photo_nodes()
        if not photos:
            self.fail('当前相册没有可预览的图片')
        photo = photos[0]
        x, y, w, h = (float(photo.get(k)) for k in ('x', 'y', 'width', 'height'))
        # 当前首行可能被导航栏部分遮挡，点击图片实际可见区域。
        self.device.click(round(x + w / 2), round((max(top, y) + y + h) / 2))
        time.sleep(2)
        if not any(re.match(r'图片\d+/\d+', n.get('label') or '')
                   for n in self.nodes() if n.get('visible') == 'true'):
            self.fail('点击图片后未进入大图预览')
