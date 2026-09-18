"""微信动态性能用例的 WDA 页面能力。"""

import logging
import os
import threading
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class WeixinCase(WdaCase):
    PACKAGE = 'com.tencent.xin'
    APP_NAME = '微信'

    IMAGE_GROUP = os.getenv('WEIXIN_IMAGE_GROUP', '性能测试图片群')
    VIDEO_GROUP = os.getenv('WEIXIN_VIDEO_GROUP', '性能测试群')
    VOICE_GROUP = os.getenv('WEIXIN_VOICE_GROUP', '性能测试语音')
    TEST_ACCOUNT = os.getenv('WEIXIN_TEST_ACCOUNT', '测试账号')
    CONTACT_NAME = os.getenv('WEIXIN_CONTACT_NAME', '测试账号')
    RECOMMEND_RECIPIENT = os.getenv(
        'WEIXIN_RECOMMEND_RECIPIENT', '文件传输助手')
    FRIEND_ACCOUNT = os.getenv('WEIXIN_FRIEND_ACCOUNT', '')
    TECH_ACCOUNT = os.getenv('WEIXIN_TECH_ACCOUNT', '华为手机')
    HARMONY_ACCOUNT = os.getenv('WEIXIN_HARMONY_ACCOUNT', 'HarmonyOS')
    TENCENT_NEWS_ACCOUNT = os.getenv(
        'WEIXIN_TENCENT_NEWS_ACCOUNT', '腾讯新闻')
    CCTV_NEWS_ACCOUNT = os.getenv('WEIXIN_CCTV_NEWS_ACCOUNT', '央视新闻')

    LUCKIN_MINI = os.getenv('WEIXIN_LUCKIN_MINI', '瑞幸咖啡')
    LUCKIN_PRODUCT = os.getenv(
        'WEIXIN_LUCKIN_PRODUCT', '生椰拿铁（首创）')
    XICHA_MINI = os.getenv('WEIXIN_XICHA_MINI', '喜茶GO')
    MEITUAN_MINI = os.getenv(
        'WEIXIN_MEITUAN_MINI', '美团丨外卖团购特价美食酒店电影')
    MIXUE_MINI = os.getenv('WEIXIN_MIXUE_MINI', '蜜雪冰城')
    JD_MINI = os.getenv('WEIXIN_JD_MINI', '京东购物丨点外卖领国补')
    TONGCHENG_MINI = os.getenv('WEIXIN_TONGCHENG_MINI', '同程旅行')

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """首尾维测点至少采集 5 秒，中间步骤不采集 trace。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
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
            logging.exception('设置微信 WDA 连续页面模式失败')

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
        if self.device.locked():
            self.device.unlock()
            time.sleep(2)
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束微信进程失败，继续启动')
        time.sleep(1)

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

    def dismiss_optional_prompts(self):
        for _ in range(6):
            nodes = self.nodes()
            prompt = self.find(
                '我知道了', '以后再说', '暂不', '取消', '关闭',
                '要求 App 不跟踪', '保留当前选择', nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(1)

    def dismiss_content_prompts(self):
        """只关闭内容弹窗，避免误点页面本身的“关闭”。"""
        for _ in range(4):
            nodes = self.nodes()
            prompt = self.find(
                '我知道了', '以后再说', '暂不', '不再提醒',
                '要求 App 不跟踪', '保留当前选择', nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(1)

    def edge_back(self, wait=2):
        back = self.find('返回', '关闭', max_y=140)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(wait)

    def bottom_tab(self, name, nodes=None):
        matches = self.matching_nodes(name, min_y=760, nodes=nodes)
        return matches[0] if matches else None

    def is_main_page(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.bottom_tab('微信', nodes=nodes) is not None
                and self.find('快捷操作', max_y=120, nodes=nodes) is not None)

    def return_weixin_home(self):
        for _ in range(12):
            nodes = self.nodes()
            weixin = self.bottom_tab('微信', nodes=nodes)
            if weixin is not None:
                self.tap_node(weixin)
                time.sleep(2)
                if self.is_main_page():
                    return
                continue
            cancel = self.find('取消', min_y=650, nodes=nodes)
            if cancel is not None:
                self.tap_node(cancel)
                time.sleep(1)
                continue
            self.edge_back(wait=1)
        self.fail('多次返回后仍未到达微信主界面，请确认账号已登录')

    def start_weixin(self):
        # trace 上下文负责补足到 5 秒；这里不额外等待，避免首步 trace
        # 因固定 sleep 被拉长。
        self.start_app(wait=0)

    def finish_weixin_start(self):
        self.dismiss_optional_prompts()
        self.return_weixin_home()

    def open_recent_mini_programs(self):
        """从微信首页下拉，进入最近/常用小程序面板。"""
        self.return_weixin_home()
        self.device.swipe(201, 150, 201, 700, 0.8)
        self.wait_for('搜索小程序', max_y=180, timeout=6)
        self.wait_for('常用的小程序', min_y=350, timeout=6)
        time.sleep(1)

    def open_common_mini_program(self, *names):
        """打开“常用的小程序”中的指定项。"""
        nodes = self.nodes()
        if self.find('常用的小程序', min_y=350, nodes=nodes) is None:
            self.open_recent_mini_programs()
            nodes = self.nodes()
        matches = self.matching_nodes(
            *names, contains=True, min_y=490, nodes=nodes)
        if not matches:
            self.fail('“常用的小程序”未找到：{}，请先将其加入常用'.format(
                ' / '.join(names)))
        self.tap_node(matches[0])
        # 小程序内容可能是 Canvas，右上角微信胶囊是稳定的就绪标志。
        self.wait_for('关闭', max_y=120, timeout=12)
        time.sleep(7)

    def dismiss_mini_program_permissions(self):
        """处理首次打开小程序时可能出现的系统权限弹窗。"""
        for _ in range(3):
            nodes = self.nodes()
            prompt = self.find(
                '使用App时允许', '允许一次', '允许', '好',
                min_y=300, nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(2)

    def close_mini_program(self):
        close = self.find('关闭', max_y=120)
        if close is None:
            self.fail('未找到小程序右上角关闭按钮')
        self.tap_node(close)
        time.sleep(3)
        self.return_weixin_home()

    def enter_mixue_order_page(self):
        # 2026-09-17 WEditor（402x874）：蜜雪冰城首次进入会出现一个
        # 不在 WDA 树中的全屏活动弹窗，关闭按钮中心为 (201, 660)。
        # 即使弹窗已消失，随后点击可访问的底部“点餐”也会校正页面状态。
        self.device.click(201, 660)
        time.sleep(1)
        self.tap('点餐', min_y=760, wait=3)
        self.dismiss_mini_program_permissions()
        nodes = self.nodes()
        if self.find('门店列表', nodes=nodes) is not None:
            stores = [node for node in nodes
                      if node.get('visible') == 'true'
                      and 430 <= float(node.get('y', 0)) <= 800
                      and ('店-No.' in self.node_name(node)
                           or self.node_name(node).endswith('店'))]
            if not stores:
                self.fail('门店列表没有可选门店，请开启定位或预置常用门店')
            stores.sort(key=lambda item: (
                float(item.get('y', 0)), float(item.get('x', 0))))
            self.tap_node(stores[0])
            time.sleep(7)

    def tongcheng_query_trains(self):
        # 同程主体由 Canvas 绘制，WDA 只暴露微信胶囊。以下坐标由
        # WEditor 在本机 402x874 竖屏下核对：火车票查询按钮中心。
        self.device.click(201, 630)
        time.sleep(8)

    def tongcheng_open_more_dates(self):
        # 火车票结果页右上角日历图标。
        self.device.click(375, 128)
        time.sleep(4)

    def tongcheng_close_dates(self):
        # 日期页底部中央关闭按钮。
        self.device.click(201, 770)
        time.sleep(3)

    def tongcheng_return_home(self):
        # 火车票结果页左上角返回箭头。
        self.device.click(22, 78)
        time.sleep(4)

    def open_chat(self, *names):
        self.return_weixin_home()
        chat = self.find(*names, contains=True, min_y=130, max_y=760)
        if chat is None:
            self.fail('消息列表未找到预置聊天：{}'.format(' / '.join(names)))
        self.tap_node(chat)
        time.sleep(3)

    def open_chat_actions(self):
        """打开聊天底部“+”功能面板，并兼容键盘已弹出的状态。"""
        for _ in range(3):
            nodes = self.nodes()
            if self.find('照片', min_y=580, nodes=nodes) is not None:
                return
            more = self.find('更多', min_y=350, nodes=nodes)
            if more is None:
                self.fail('好友聊天页面没有底部“+”按钮')
            self.tap_node(more)
            time.sleep(2)
        self.fail('多次点击后仍未打开聊天更多功能面板')

    def open_photo_picker(self):
        self.open_chat_actions()
        self.tap('照片', min_y=580, wait=4)
        nodes = self.nodes()
        permission = self.find(
            '允许完全访问', '允许访问所有照片', '好', nodes=nodes)
        if permission is not None:
            self.tap_node(permission)
            time.sleep(4)
        self.wait_for('最近项目', '关闭', max_y=120, timeout=8)

    def chat_swipe_down(self, count):
        for _ in range(count):
            self.device.swipe(0.5, 0.35, 0.5, 0.75, 0.3)
            time.sleep(1)

    def open_chat_media(self, media_name):
        candidates = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeOther'
                      and media_name in self.node_name(node)
                      and 80 <= float(node.get('y', 0)) <= 760
                      and float(node.get('height', 0)) >= 80]
        if not candidates:
            self.fail('当前聊天没有可查看的{}消息'.format(media_name))
        node = sorted(candidates, key=lambda item: float(item.get('y', 0)))[0]
        name = self.node_name(node)
        y = round(float(node.get('y', 0)) + min(
            float(node.get('height', 0)) / 2, 100))
        # 2026-09-17 WEditor（402x874）：聊天媒体容器覆盖整行，
        # 收到的媒体在左侧，发出的媒体在右侧，媒体本身不单独暴露。
        self.device.click(110 if not name.startswith('我') else 292, y)
        time.sleep(3)

    def horizontal_browse(self, right, left):
        for start, end, count in ((0.18, 0.82, right),
                                  (0.82, 0.18, left)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.3)
                time.sleep(1)

    def long_press_current_media(self):
        self.device.tap_hold(201, 430, 1.2)
        time.sleep(2)

    def play_first_voice(self):
        voices = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and '语音' in self.node_name(node)
                  and 90 <= float(node.get('y', 0)) <= 760
                  and float(node.get('height', 0)) >= 40]
        if not voices:
            self.fail('性能测试语音群中没有预置语音消息')
        node = sorted(voices, key=lambda item: float(item.get('y', 0)))[0]
        name = self.node_name(node)
        x = 110 if not name.startswith('我') else 292
        y = round(float(node.get('y', 0)) + float(node.get('height', 0)) / 2)
        self.device.click(x, y)
        time.sleep(3)

    def open_moments_camera_menu(self):
        self.tap('拍照', max_y=120, wait=1)
        prompt = self.find('我知道了')
        if prompt is not None:
            self.tap_node(prompt)
            time.sleep(1)
            self.tap('拍照', max_y=120, wait=1)

    def comment_first_moment(self, text):
        operations = self.matching_nodes('Moments_OperationButton')
        if not operations:
            self.fail('朋友圈当前可见区域没有可评论的动态')
        self.tap_node(operations[0])
        time.sleep(1)
        self.tap('评论', min_y=100, wait=1)
        self.enter_text(text)
        self.tap('Send', '发送', min_y=700, wait=3)

    def select_photos(self, count):
        photos = []
        seen = set()
        for node in self.nodes():
            name = self.node_name(node)
            if (node.get('visible') != 'true'
                    or node.tag != 'XCUIElementTypeImage'
                    or not name.startswith('照片')):
                continue
            rect = tuple(node.get(key) for key in ('x', 'y', 'width', 'height'))
            if rect not in seen:
                seen.add(rect)
                photos.append(node)
        photos.sort(key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))
        if len(photos) < count:
            self.fail('相册至少需要预置{}张照片，当前仅找到{}张'.format(
                count, len(photos)))
        for node in photos[:count]:
            # 微信 iOS 相册中，点缩略图主体会进入大图预览；右上角圆圈
            # 才是多选控件。WDA 未单独暴露圆圈，因此按缩略图矩形定位。
            x = float(node.get('x', 0)) + float(node.get('width', 0)) - 20
            y = float(node.get('y', 0)) + 20
            self.device.click(round(x), round(y))
            time.sleep(0.4)

    def open_first_photo_preview(self):
        photos = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeImage'
                  and self.node_name(node).startswith('照片')]
        if not photos:
            self.fail('相册中没有可预览的照片')
        photos.sort(key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))
        self.tap_node(photos[0])
        self.wait_for('勾选框', max_y=120, timeout=5)
        time.sleep(2)

    def open_contacts(self):
        self.return_weixin_home()
        self.tap('通讯录', min_y=760, wait=2)

    def open_contact(self, name):
        contacts = self.matching_nodes(name, min_y=130, max_y=780)
        if not contacts:
            self.fail('通讯录未找到联系人“{}”'.format(name))
        self.tap_node(contacts[0])
        time.sleep(3)

    def view_contact_avatar(self):
        # WEditor：好友头像没有可访问性名称，固定在资料页左上区域。
        self.device.click(51, 139)
        time.sleep(2)
        self.edge_back(wait=2)

    def open_contact_moments_picture(self):
        moment = self.find('朋友圈', min_y=180, max_y=420)
        if moment is None:
            self.fail('好友资料页没有朋友圈入口，请检查朋友圈权限')
        self.tap_node(moment)
        time.sleep(3)
        rows = [node for node in self.nodes()
                if node.get('visible') == 'true'
                and node.tag == 'XCUIElementTypeOther'
                and '图片' in self.node_name(node)
                and 430 <= float(node.get('y', 0)) <= 840]
        if not rows:
            self.fail('好友朋友圈没有预置图片动态')
        self.tap_node(sorted(rows, key=lambda item: float(item.get('y', 0)))[0])
        time.sleep(3)
        picture = self.find('图片, 1/', contains=True, min_y=100, max_y=700)
        if picture is None:
            self.fail('朋友圈动态中没有可浏览的图片')
        self.tap_node(picture)
        time.sleep(3)

    def return_contact_profile(self, contact_name):
        for _ in range(5):
            nodes = self.nodes()
            if (self.find(contact_name, nodes=nodes) is not None
                    and self.find('朋友圈', nodes=nodes) is not None
                    and self.find('发消息', nodes=nodes) is not None):
                return
            self.edge_back(wait=1)
        self.fail('未能返回好友资料页')

    def recommend_contact(self, recipient):
        self.tap('更多', max_y=120, wait=2)
        self.tap('把他(她)推荐给朋友', contains=True, wait=2)
        self.tap(recipient, contains=True, min_y=180, max_y=760, wait=2)
        self.tap('发送', min_y=700, wait=3)

    def choose_first_photo(self):
        photos = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag == 'XCUIElementTypeImage'
                  and self.node_name(node).startswith('照片')]
        if not photos:
            self.fail('相册中没有可供扫一扫识别的照片')
        photos.sort(key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))
        self.tap_node(photos[0])
        time.sleep(4)

    def tap_chat_input(self):
        # WEditor：聊天输入框无独立可访问节点，位于底部中间。
        self.device.click(180, 812)
        time.sleep(1)

    def send_voice_message(self, duration=2):
        self.tap('语音', min_y=400, wait=1)
        button = self.wait_for('按住 说话', '按住说话', contains=True,
                               min_y=400, timeout=5)
        x = round(float(button.get('x', 0)) + float(button.get('width', 0)) / 2)
        y = round(float(button.get('y', 0)) + float(button.get('height', 0)) / 2)
        self.device.tap_hold(x, y, duration)
        time.sleep(2)

    def return_weixin_chat(self):
        for _ in range(5):
            nodes = self.nodes()
            if (self.find('语音', min_y=350, nodes=nodes) is not None
                    and self.find('表情', min_y=350, nodes=nodes) is not None
                    and self.find('更多', min_y=350, nodes=nodes) is not None):
                time.sleep(2)
                return
            self.edge_back(wait=1)
        self.fail('通话结束后未返回微信聊天页')

    def open_official_account(self, name):
        account = self.find(name, min_y=120, max_y=780)
        if account is not None:
            self.tap_node(account)
            time.sleep(4)
            return
        # 当前实机中“华为手机”属于服务号。Excel 写的是先点公众号，
        # 因而在公众号列表找不到时退回通讯录的服务号列表继续同一目标。
        self.edge_back(wait=1)
        service = self.find('服务号', min_y=350, max_y=520)
        if service is None:
            self.fail('公众号/服务号列表均未找到“{}”'.format(name))
        self.tap_node(service)
        time.sleep(2)
        account = self.find(name, min_y=120, max_y=780)
        if account is None:
            self.fail('请预先关注公众号或服务号“{}”'.format(name))
        self.tap_node(account)
        time.sleep(4)

    def open_first_official_article(self):
        articles = [node for node in self.nodes()
                    if node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeCell',
                                     'XCUIElementTypeButton')
                    and 100 <= float(node.get('y', 0)) <= 780
                    and float(node.get('width', 0)) >= 300
                    and float(node.get('height', 0)) >= 70]
        if not articles:
            self.fail('公众号/服务号页面当前没有可打开的文章')
        self.tap_node(sorted(
            articles, key=lambda item: float(item.get('y', 0)))[0])
        time.sleep(5)

    def open_first_official_message(self):
        """打开公众号对话页当前可见的第一篇图文消息。"""
        messages = [node for node in self.nodes()
                    if node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeButton',
                                     'XCUIElementTypeCell')
                    and 100 <= float(node.get('y', 0)) <= 760
                    and float(node.get('width', 0)) >= 300
                    and float(node.get('height', 0)) >= 70]
        if not messages:
            self.fail('公众号对话页当前没有可打开的图文消息')
        messages.sort(key=lambda item: float(item.get('y', 0)))
        self.tap_node(messages[0])
        time.sleep(7)

    def open_official_feature(self, names, fallback_names=()):
        """打开公众号菜单；菜单改版或失效时改看最新图文。"""
        nodes = self.nodes()
        item = self.find(*names, min_y=760, nodes=nodes)
        used_name = names[0]
        if item is None and fallback_names:
            item = self.find(*fallback_names, min_y=760, nodes=nodes)
            if item is not None:
                used_name = fallback_names[0]
                logging.warning('公众号菜单“%s”已改版，改用“%s”',
                                names[0], used_name)
        if item is None:
            logging.warning('公众号菜单“%s”不可用，改为打开最新可见图文', names[0])
            self.open_first_official_message()
            return
        self.tap_node(item)
        time.sleep(7)
        nodes = self.nodes()
        # 个别公众号菜单仍显示但链接已经失效，点击后会停留在对话页。
        if (self.find('发消息', min_y=760, nodes=nodes) is not None
                and self.find(used_name, min_y=760, nodes=nodes) is not None):
            logging.warning('公众号菜单“%s”点击后未跳转，改看最新可见图文', used_name)
            self.open_first_official_message()

    def return_official_profile(self, account_name):
        for _ in range(5):
            nodes = self.nodes()
            if (self.find(account_name, nodes=nodes) is not None
                    and (self.find('私信', nodes=nodes) is not None
                         or self.find('不再关注', nodes=nodes) is not None
                         or self.find('发消息', min_y=740,
                                      nodes=nodes) is not None)):
                return
            self.edge_back(wait=2)
        self.fail('未能返回公众号资料页：{}'.format(account_name))

    def return_official_list(self):
        for _ in range(5):
            nodes = self.nodes()
            search_fields = [node for node in nodes
                             if node.get('visible') == 'true'
                             and node.tag == 'XCUIElementTypeSearchField'
                             and self.node_name(node) == '搜索'
                             and float(node.get('y', 0)) <= 180]
            if (search_fields
                    and (self.find('添加', max_y=120, nodes=nodes) is not None
                         or self.find('更多', max_y=120, nodes=nodes) is not None)):
                return
            self.edge_back(wait=1)
        self.fail('未能返回公众号或服务号列表')

    def return_contacts(self):
        for _ in range(5):
            nodes = self.nodes()
            if (self.bottom_tab('通讯录', nodes=nodes) is not None
                    and self.find('公众号', nodes=nodes) is not None):
                return
            self.edge_back(wait=1)
        self.fail('未能返回通讯录')

    def open_official_chat(self):
        private = self.find('私信')
        if private is not None:
            self.tap_node(private)
            time.sleep(3)

    def open_subscription_feed(self):
        self.return_weixin_home()
        entry = self.find('订阅号', '公众号', min_y=130, max_y=780)
        if entry is None:
            self.fail('微信消息列表没有订阅号/公众号入口')
        self.tap_node(entry)
        time.sleep(5)

    def open_subscription_account(self, account_name):
        """从新版公众号信息流进入指定已关注账号。"""
        nodes = self.nodes()
        account = self.find(account_name, contains=True, nodes=nodes)
        if account is not None:
            self.tap_node(account)
            time.sleep(5)
            return
        # 新版公众号信息流主体为 Canvas。右上角头像入口固定在 402x874
        # 竖屏的 (375, 78)，进入“关注”后账号列表重新具备可访问性。
        self.device.click(375, 78)
        time.sleep(3)
        self.tap('关注', min_y=90, max_y=190, wait=3)
        account = self.find(account_name, contains=True, min_y=130)
        if account is None:
            self.fail('关注列表未找到公众号“{}”'.format(account_name))
        self.tap_node(account)
        time.sleep(5)

    def open_first_favorite(self):
        nodes = self.nodes()
        if self.find('没有任何收藏', contains=True, nodes=nodes) is not None:
            self.fail('收藏为空，请预先收藏至少一条可打开的内容')
        entries = [node for node in nodes
                   if node.get('visible') == 'true'
                   and node.tag in ('XCUIElementTypeCell',
                                    'XCUIElementTypeButton')
                   and 100 <= float(node.get('y', 0)) <= 780
                   and float(node.get('width', 0)) >= 280
                   and float(node.get('height', 0)) >= 50]
        if not entries:
            self.fail('收藏页面没有找到可打开的收藏条目')
        entries.sort(key=lambda item: float(item.get('y', 0)))
        self.tap_node(entries[0])
        time.sleep(5)

    def return_me_page(self):
        self.return_weixin_home()
        self.tap('我', min_y=760, wait=3)

    def open_general_settings(self):
        nodes = self.nodes()
        if self.find('存储空间', nodes=nodes) is not None:
            # 当前微信将原“通用”页拆成设置页里的“通用”分区标题。
            logging.warning('当前微信无独立“通用”页面，继续使用设置页的通用分区')
            return
        self.tap('通用', min_y=100, max_y=760, wait=3)

    def open_chat_camera(self):
        """从好友聊天的“+”面板打开相机。"""
        self.open_chat_actions()
        self.tap('拍摄', min_y=580, wait=3)
        for _ in range(4):
            nodes = self.nodes()
            if self.find('拍照', min_y=650, nodes=nodes) is not None:
                return
            permission = self.find(
                '使用App时允许', '仅在使用中允许', '允许一次',
                '允许', '好', min_y=250, nodes=nodes)
            if permission is None:
                break
            self.tap_node(permission)
            time.sleep(2)
        self.wait_for('拍照', min_y=650, timeout=8)

    def start_chat_video_recording(self, duration=4):
        """新版微信没有单独“录像”页签，长按快门录制。"""
        if self.find('拍照', min_y=650) is None:
            self.fail('相机快门未就绪')
        self._video_record_error = None

        def record():
            try:
                self.device.tap_hold(201, 777, duration)
            except Exception as error:  # 在主线程汇总 WDA 异常
                self._video_record_error = error

        self._video_record_thread = threading.Thread(
            target=record, name='weixin-video-record', daemon=True)
        self._video_record_thread.start()
        time.sleep(1)

    def stop_chat_video_recording(self):
        thread = getattr(self, '_video_record_thread', None)
        if thread is None:
            self.fail('录像未开始')
        thread.join(timeout=12)
        if thread.is_alive():
            self.fail('录像长按操作未在预期时间内结束')
        if self._video_record_error is not None:
            raise self._video_record_error
        self.wait_for('发送', min_y=650, timeout=8)

    def choose_first_moment_location(self):
        """在朋友圈位置页选第一个具体地点并完成。"""
        nodes = self.nodes()
        excluded = ('不显示位置', '上海市', '完成', '搜索地点')
        candidates = [node for node in nodes
                      if node.get('visible') == 'true'
                      and node.tag == 'XCUIElementTypeStaticText'
                      and 230 <= float(node.get('y', 0)) <= 760
                      and self.node_name(node) not in excluded
                      and not self.node_name(node).startswith('上海市')]
        if not candidates:
            self.fail('位置页没有可选的具体地点，请开启定位')
        candidates.sort(key=lambda item: (
            float(item.get('y', 0)), float(item.get('x', 0))))
        self.tap_node(candidates[0])
        time.sleep(2)
        self.tap('完成', max_y=120, wait=3)

    def dismiss_luckin_prompts(self):
        """处理瑞幸首次隐私同意和最近门店提示。"""
        nodes = self.nodes()
        if self.find('瑞幸咖啡温馨提示', contains=True, nodes=nodes) is not None:
            # Canvas 弹窗虽暴露文字，文字节点本身不响应点击。
            self.device.click(280, 500)
            time.sleep(5)
        self.dismiss_mini_program_permissions()
        nodes = self.nodes()
        if self.find('距你最近的门店', contains=True, nodes=nodes) is not None:
            self.device.click(361, 546)
            time.sleep(2)

    def open_luckin_menu(self):
        self.dismiss_luckin_prompts()
        self.tap('菜单', min_y=760, wait=5)
        self.dismiss_luckin_prompts()

    def open_luckin_first_product(self):
        product = self.find(
            self.LUCKIN_PRODUCT, contains=True, min_y=130, max_y=760)
        if product is None:
            self.fail('人气Top中未找到预置商品“{}”'.format(
                self.LUCKIN_PRODUCT))
        self.tap_node(product)
        self.wait_for('加入购物车', min_y=700, timeout=10)

    def return_discover(self):
        """从视频号、直播间或小程序返回发现页。"""
        for _ in range(8):
            nodes = self.nodes()
            discover = self.bottom_tab('发现', nodes=nodes)
            if (discover is not None
                    and self.find('视频号', nodes=nodes) is not None
                    and self.find('直播', nodes=nodes) is not None):
                return
            close = self.find('关闭', max_y=120, nodes=nodes)
            back = self.find('返回', max_y=120, nodes=nodes)
            if close is not None:
                self.tap_node(close)
            elif back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(4, 437, 354, 437, 0.3)
            time.sleep(2)
        self.fail('未能返回发现页')

    def open_first_live(self):
        cells = [node for node in self.nodes()
                 if node.get('visible') == 'true'
                 and self.node_name(node).startswith(
                     'LiveHomePageNormalCell_')]
        if not cells:
            self.fail('直播页当前没有可打开的直播')
        cells.sort(key=lambda item: float(item.get('y', 0)))
        self.tap_node(cells[0])
        time.sleep(5)

    def return_service_page(self):
        for _ in range(6):
            nodes = self.nodes()
            if (self.find('手机充值', nodes=nodes) is not None
                    and self.find('生活缴费', nodes=nodes) is not None):
                return
            close = self.find('关闭', max_y=120, nodes=nodes)
            if close is not None:
                self.tap_node(close)
            else:
                self.edge_back(wait=0)
            time.sleep(2)
        self.fail('未能返回服务页')

    def accept_payment_prompts(self):
        """同意充值/缴费小程序的首次协议和定位权限。"""
        for _ in range(5):
            nodes = self.nodes()
            prompt = self.find(
                '同意', '允许', '使用App时允许',
                min_y=250, nodes=nodes)
            if prompt is None:
                return
            self.tap_node(prompt)
            time.sleep(3)

    def prepare_utility_city(self):
        self.accept_payment_prompts()
        nodes = self.nodes()
        choose = self.find('选择城市', nodes=nodes)
        if choose is not None:
            self.tap_node(choose)
            time.sleep(3)
            self.tap('上海市', contains=True, min_y=100, wait=5)
        self.wait_for('电费', timeout=10)

    def select_first_utility_company(self):
        companies = self.matching_nodes(
            '缴费单位', contains=True, min_y=100, max_y=780)
        companies = [node for node in companies
                     if self.node_name(node) != '缴费单位']
        if not companies:
            self.fail('电费页没有可选的缴费单位')
        self.tap_node(companies[0])
        time.sleep(4)
