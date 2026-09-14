"""抖音动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class DouyinCase(WdaCase):
    PACKAGE = 'com.ss.iphone.ugc.Aweme'
    APP_NAME = '抖音'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """为本批抖音用例把首尾维测打点补足到 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                remaining = 5 - (time.monotonic() - started_at)
                if remaining > 0:
                    time.sleep(remaining)

    def _enable_continuous_ui_mode(self):
        """避免视频流和直播让 XCTest 一直等待页面进入 idle。"""
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

    def _restore_idle_settings(self):
        previous = getattr(self, '_previous_idle_settings', None)
        if previous is None:
            return
        try:
            self.device.appium_settings(previous)
        except Exception:
            logging.exception('恢复 WDA idle 等待设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        """冷启动可让每轮都从首页开始，且不把清理动作记入首步 trace。"""
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束抖音进程失败，继续尝试启动')
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

    def _dismiss_optional_prompts(self):
        for _ in range(4):
            nodes = self.nodes()
            button = self.find(
                '不允许', '以后再说', '我知道了', '暂不', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(1)

    def start_douyin(self):
        self.start_app(wait=5)
        self.normalize_home_after_launch()

    def normalize_home_after_launch(self):
        """启动 trace 结束后处理非性能步骤并统一回到推荐页。"""
        self._dismiss_optional_prompts()
        self.return_main()

    def swipe_up_times(self, count, pause=1):
        for _ in range(count):
            self.device.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
            time.sleep(pause)

    def swipe_down_times(self, count, pause=1):
        for _ in range(count):
            self.device.swipe(0.5, 0.35, 0.5, 0.75, 0.3)
            time.sleep(pause)

    def return_main(self):
        """退出浮层或子页面，回到首页的推荐视频流。"""
        for _ in range(12):
            nodes = self.nodes()
            home = self.find('首页', min_y=740, nodes=nodes)
            if home is not None:
                self.tap_node(home)
                time.sleep(2)
                nodes = self.nodes()
                recommend = self.find('推荐', max_y=130, nodes=nodes)
                if recommend is not None:
                    self.tap_node(recommend)
                    time.sleep(3)
                else:
                    back_to_recommend = self.find(
                        '返回推荐', max_y=130, nodes=nodes)
                    if back_to_recommend is not None:
                        self.tap_node(back_to_recommend)
                        time.sleep(4)
                return

            # 钱包可能自动弹出实名提现面板；该面板的关闭按钮未暴露名称。
            if self.find('确认是本人提现', nodes=nodes) is not None:
                self.device.click(28, 384)
                time.sleep(2)
                continue

            discard = self.find(
                '不保存返回', '放弃', '不保存', '确认退出', nodes=nodes)
            if discard is not None:
                self.tap_node(discard)
                time.sleep(3)
                continue

            close = self.find(
                'CommentPanelCloseButton', '关闭', max_y=760, nodes=nodes)
            if close is not None:
                self.tap_node(close)
                time.sleep(2)
                continue

            back = self.find(
                '返回推荐', '返回', '返回。按钮', max_y=140, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(2)
        self.fail('多次返回后仍未到达抖音主界面')

    def _top_channel_nodes(self, names, nodes):
        return [node for node in nodes
                if node.tag == 'XCUIElementTypeButton'
                and 55 <= float(node.get('y', 0)) <= 115
                and self.node_name(node) in names]

    def select_top_channel(self, *names, wait=6):
        """滚动顶部频道并点击；兼容屏外但仍存在于 WDA 树中的频道。"""
        for _ in range(12):
            nodes = self.nodes()
            channels = self._top_channel_nodes(names, nodes)
            visible = [node for node in channels
                       if node.get('visible') == 'true'
                       and 0 <= float(node.get('x', 0)) < 350]
            if visible:
                self.tap_node(visible[0])
                time.sleep(wait)
                return
            if channels:
                target_x = float(channels[0].get('x', 0))
                if target_x < 0:
                    self.device.swipe(40, 430, 360, 430, 0.2)
                else:
                    self.device.swipe(360, 430, 40, 430, 0.2)
                time.sleep(2)
                continue
            self.fail('顶部频道不存在：{}'.format(' / '.join(names)))
        self.fail('多次滑动后仍未显示顶部频道：{}'.format(' / '.join(names)))

    def open_featured(self):
        # 工作簿称“长视频”，2026-09-12 当前版本显示为“精选”。
        self.select_top_channel('精选', '长视频')
        self.wait_for('精选', '长视频', max_y=120, timeout=10)

    def open_experience(self):
        self.select_top_channel('经验')
        self.wait_for('经验', max_y=120, timeout=10)

    def open_hotspot(self):
        self.select_top_channel('热点')
        self.wait_for('热点', max_y=120, timeout=10)

    def open_recommend(self):
        # 子页面可能完全移除顶部频道树，统一复用多层返回逻辑更稳定。
        self.return_main()

    def open_follow_channel(self):
        self.select_top_channel('关注')
        self.wait_for('关注', max_y=120, timeout=10)

    def _fail_if_media_permission_prompt(self):
        prompts = {
            '想访问相机': '请先在系统设置中允许抖音访问相机',
            '想访问麦克风': '请先在系统设置中允许抖音访问麦克风',
            '想完全访问你的照片图库': '请先允许抖音完全访问照片图库',
        }
        for node in self.nodes():
            name = self.node_name(node)
            for marker, message in prompts.items():
                if marker in name:
                    self.fail(message)

    def open_creation(self):
        self.tap('btn home add', 'btn home add hollow',
                 min_y=760, wait=4)
        self._fail_if_media_permission_prompt()
        self.wait_for('相册', min_y=650, timeout=10)

    def open_creation_album(self):
        self.tap('相册', min_y=650, wait=4)
        self._fail_if_media_permission_prompt()
        self.wait_for('关闭相册', timeout=10)

    def close_creation_album(self):
        self.tap('关闭相册', max_y=130, wait=3)
        self.wait_for('(animatedRecordButton)', timeout=10)

    def select_creation_photo_mode(self):
        nodes = self.nodes()
        mode = self.find('已选择照片', '未选择照片',
                         min_y=600, max_y=700, nodes=nodes)
        if mode is None:
            mode = self.find('照片', min_y=600, max_y=700, nodes=nodes)
        if mode is None:
            self.fail('拍摄页未找到“照片”模式')
        self.tap_node(mode)
        time.sleep(2)

    def _record_button(self):
        nodes = self.nodes()
        button = self.find('(animatedRecordButton)', nodes=nodes)
        if button is not None:
            return button
        candidates = []
        for node in nodes:
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and 130 <= x <= 210 and 570 <= y <= 760
                    and 60 <= width <= 110 and 60 <= height <= 110):
                candidates.append(node)
        if not candidates:
            self.fail('拍摄页未找到快门按钮')
        return candidates[0]

    def take_creation_photo(self):
        self.tap_node(self._record_button())
        time.sleep(6)
        self.wait_for('下一步', min_y=760, timeout=12)

    def open_photo_music(self):
        nodes = self.nodes()
        music = self.find('选择音乐', max_y=130, nodes=nodes)
        if music is None:
            music = self.find('BGM', contains=True, max_y=130, nodes=nodes)
        if music is None:
            # 已自动套用推荐音乐时，入口会直接显示歌名，旁边另有
            # “智能生歌”和“取消选择”。用顶部中间按钮的几何范围识别歌名，
            # 避免把右侧编辑工具或返回按钮误当作配乐入口。
            candidates = []
            ignored = {'返回', '智能生歌', '取消选择', '设置'}
            for node in nodes:
                name = self.node_name(node)
                x, y, width = (float(node.get(key, 0))
                               for key in ('x', 'y', 'width'))
                if (node.get('visible') == 'true'
                        and node.tag == 'XCUIElementTypeButton'
                        and name not in ignored
                        and 145 <= x <= 260 and 55 <= y <= 115
                        and 70 <= width <= 150):
                    candidates.append(node)
            if candidates:
                music = candidates[0]
        if music is None:
            self.fail('照片编辑页未找到配乐入口')
        self.tap_node(music)
        time.sleep(5)
        self.wait_for('搜索歌名/歌手/歌词/情绪', timeout=10)

    def close_photo_music(self):
        self.tap('关闭配乐面板', wait=3)
        self.wait_for('下一步', min_y=760, timeout=10)

    def next_from_photo_editor(self):
        self.tap('下一步', min_y=760, wait=6)
        self.wait_for('预览', max_y=130, timeout=12)

    def preview_post(self):
        self.tap('预览', max_y=130, wait=4)
        self.wait_for('设为封面', min_y=760, timeout=10)

    def discard_creation_and_return_home(self):
        # 预览返回发布页后会继续退到照片编辑页。该页左上角返回菜单是
        # 短暂出现的悬浮层，完整 source 往往在菜单消失后才返回，因此要
        # 立即通过 WDA 元素查询点击“不保存返回”，不能交给通用慢轮询。
        nodes = self.nodes()
        if (self.find('下一步', min_y=760, nodes=nodes) is not None
                and self.find('设置', max_y=130, nodes=nodes) is not None):
            self.device.click(0.05, 0.08)
            time.sleep(0.1)
            discard = self.device(name='不保存返回')
            if discard.exists:
                discard.click()
                time.sleep(4)
        self.return_main()

    def open_messages(self):
        self.tap('消息', min_y=760, wait=6)
        self.wait_for('消息', max_y=130, timeout=10)

    def open_test_chat(self):
        candidates = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and self.node_name(node).strip().casefold() == 'test'
                      and 250 <= float(node.get('y', 0)) <= 760]
        if not candidates:
            # 刚互关后会话标题“Test”可能只被视觉绘制，WDA 仅暴露这条
            # 系统摘要；点击摘要仍会命中同一会话行。
            candidates = [node for node in self.nodes()
                          if node.get('visible') == 'true'
                          and '我们已互相关注，可以开始聊天了'
                          in self.node_name(node)
                          and 250 <= float(node.get('y', 0)) <= 760]
        if not candidates:
            self.fail('消息列表中未找到测试账号 Test')
        self.tap_node(candidates[0])
        time.sleep(6)
        self.wait_for('Test', max_y=130, timeout=10)

    def send_chat_text(self, text):
        fields = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and node.tag in ('XCUIElementTypeTextField',
                                   'XCUIElementTypeTextView')]
        if not fields:
            self.fail('Test 会话没有可用输入框，请确认对方已回复并允许私信')
        self.enter_text(text, clear=True)
        nodes = self.nodes()
        send = self.find('发送', min_y=720, nodes=nodes)
        if send is None:
            self.fail('输入后未出现发送按钮，请先让 Test 回复一次')
        self.tap_node(send)
        time.sleep(3)

    def send_dynamic_emoji(self):
        # 键盘或表情面板展开后工具栏会上移到约 y=449。
        self.tap('表情', min_y=400, wait=3)
        nodes = self.nodes()
        quick_emoji = self.find('比心', min_y=560, nodes=nodes)
        if quick_emoji is not None:
            # 互相关注后的新版会话直接在表情面板顶部显示动态表情。
            self.tap_node(quick_emoji)
            time.sleep(3)
            return
        # 旧版面板需要先切换到“互动表情”分类。
        self.tap('互动表情', min_y=470, wait=2)
        self.tap('比心', min_y=560, wait=3)

    def open_chat_more(self):
        nodes = self.nodes()
        if (self.find('拍摄', min_y=540, nodes=nodes) is not None
                and self.find('相册', min_y=540, nodes=nodes) is not None):
            return
        self.tap('更多面板', min_y=430, wait=3)
        self.wait_for('拍摄', min_y=540, timeout=8)

    def enter_chat_camera(self):
        self.open_chat_more()
        self.tap('拍摄', min_y=540, wait=5)
        self._fail_if_media_permission_prompt()
        self.wait_for('(animatedRecordButton)', '照片', '视频',
                      contains=True, timeout=10)

    def capture_chat_photo(self):
        nodes = self.nodes()
        photo = self.find('照片', min_y=560, nodes=nodes)
        if photo is not None:
            self.tap_node(photo)
            time.sleep(1)
        self.tap_node(self._record_button())
        time.sleep(5)
        self.wait_for('发送', '使用照片', min_y=650, timeout=10)

    def capture_chat_video(self, duration=5):
        nodes = self.nodes()
        video = self.find('视频', min_y=560, nodes=nodes)
        if video is None:
            self.fail('聊天拍摄页未找到“视频”模式')
        self.tap_node(video)
        time.sleep(2)
        button = self._record_button()
        x, y, width, height = (float(button.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        self.device.tap_hold(round(x + width / 2), round(y + height / 2),
                             duration=duration)
        time.sleep(4)
        self.wait_for('发送', '使用视频', min_y=650, timeout=10)

    def send_chat_media(self):
        self.tap('发送', '使用照片', '使用视频', contains=True,
                 min_y=650, wait=5)
        self.wait_for('Test', max_y=130, timeout=10)

    def enter_chat_album(self):
        self.open_chat_more()
        self.tap('相册', min_y=540, wait=5)
        self._fail_if_media_permission_prompt()
        self.wait_for('最近项目', '关闭相册', timeout=10)

    def select_first_album_photo(self):
        photos = [node for node in self.nodes()
                  if node.get('visible') == 'true'
                  and self.node_name(node) == 'icon_checkbox_unselect'
                  and float(node.get('y', 0)) >= 200]
        if photos:
            photos.sort(key=lambda node: (
                float(node.get('y', 0)), float(node.get('x', 0))))
            self.tap_node(photos[0])
        else:
            logging.warning('相册缩略图未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(67, 286)
        time.sleep(3)
        self.wait_for('发送', '完成', contains=True, min_y=700, timeout=10)

    def select_test_in_share_panel(self):
        self.tap('分享', max_y=760, wait=4)
        candidates = [node for node in self.nodes()
                      if node.get('visible') == 'true'
                      and self.node_name(node).strip().casefold() == 'test'
                      and 540 <= float(node.get('y', 0)) <= 740]
        if not candidates:
            self.fail('分享面板中未找到测试账号 Test')
        self.tap_node(candidates[0])
        time.sleep(3)
        self.wait_for('发送', contains=True, min_y=650, timeout=8)

    def send_selected_share(self):
        self.tap('发送', contains=True, min_y=650, wait=5)

    def open_comments(self):
        self.tap('评论', max_y=700, wait=3)
        self.wait_for('CommentInputViewTextView',
                      '发条评论，和大家一起讨论', timeout=8)

    def browse_comments_once(self, close_after):
        self.swipe_up_times(1)
        time.sleep(1)
        if close_after:
            self.tap('CommentPanelCloseButton', wait=2)

    def focus_comment_input(self):
        self.tap('CommentInputViewTextView',
                 '发条评论，和大家一起讨论', wait=1)
        self.wait_for('CommentInputViewSendButton', timeout=6)

    def enter_comment(self, text):
        self.enter_text(text, clear=True)

    def send_comment(self):
        self.tap('CommentInputViewSendButton', '发送', wait=2)

    def open_live_page(self):
        self.select_top_channel('直播', wait=5)
        # 中部频道名会随推荐状态显示“你的关注”或“直播发现”。
        self.wait_for('你的关注', '直播发现', '返回推荐',
                      max_y=180, timeout=10)

    def enter_live_room(self):
        # 2026-09-12 weditor（402×874）：直播预览的“自动进入直播间”
        # 由视频层自绘，稳定点击区域中心为 (201, 490)。
        self.device.click(201, 490)
        time.sleep(7)
        self.wait_for('直播间评论框', '购物车', timeout=12, contains=True)

    def open_live_cart(self):
        for _ in range(8):
            nodes = self.nodes()
            cart = self.find('购物车', contains=True, nodes=nodes)
            if cart is not None:
                self.tap_node(cart)
                time.sleep(5)
                self.wait_for('搜商品/序号', '全部', timeout=10)
                return
            logging.warning('当前直播间没有小黄车，继续上滑查找带货直播间')
            self.swipe_up_times(1, pause=3)
        # 直播推荐流是动态数据；连续几场都没有小黄车时，再从直播搜索页
        # 优先寻找华为相关直播，并允许使用其他可用直播作为恢复路径。
        logging.warning('随机直播均无小黄车，改从直播搜索结果寻找带货直播')
        self.return_main()
        self.tap('aweme.feed.top_bar.search_entry', max_y=130, wait=3)
        self.wait_for('aweme.search.search_bar.input', timeout=8)
        self.enter_text('华为终端', clear=True)
        self.tap('搜索', max_y=130, wait=7)
        nodes = self.nodes()
        live_tab = self.find('aweme.search.result.tab.live', nodes=nodes)
        if live_tab is not None:
            self.tap_node(live_tab)
            time.sleep(5)
            nodes = self.nodes()
        live_cards = [node for node in nodes
                      if node.get('visible') == 'true'
                      and '直播中' in self.node_name(node)
                      and 180 <= float(node.get('y', 0)) <= 780]
        if not live_cards:
            self.fail('连续8个直播间没有小黄车，搜索页也没有可用直播')
        live_cards.sort(key=lambda node: (
            '华为' not in self.node_name(node),
            float(node.get('y', 0)), float(node.get('x', 0))))
        self.tap_node(live_cards[0])
        time.sleep(7)
        cart = self.wait_for('购物车', contains=True, timeout=12)
        self.tap_node(cart)
        time.sleep(5)
        self.wait_for('搜商品/序号', '全部', timeout=10)

    def open_mall(self):
        self.tap('商城', max_y=130, wait=6)
        self.wait_for('我的订单', contains=True, max_y=260, timeout=12)

    def search_mall_product(self, keyword):
        nodes = self.nodes()
        search_bar = self.find(
            '搜索栏', contains=True, max_y=170, nodes=nodes)
        if search_bar is None:
            self.fail('商城首页未找到搜索栏')
        self.tap_node(search_bar)
        time.sleep(3)
        self.wait_for('搜索', max_y=130)
        self.enter_text(keyword, clear=True)
        self.tap('搜索', max_y=130, wait=7)

    @staticmethod
    def _is_mall_product_card(node):
        x, y, width, height = (float(node.get(key, 0))
                               for key in ('x', 'y', 'width', 'height'))
        return (node.get('visible') == 'true'
                and node.tag == 'XCUIElementTypeOther'
                and x <= 10 and 200 <= y < 790
                and width >= 380 and 100 <= height <= 180)

    def open_first_mall_product(self):
        deadline = time.monotonic() + 12
        while True:
            cards = [node for node in self.nodes()
                     if self._is_mall_product_card(node)]
            if cards:
                cards.sort(key=lambda node: float(node.get('y', 0)))
                preferred = [card for card in cards if any(
                    '北斗卫星消息版' in self.node_name(child)
                    for child in card.iter())]
                self.tap_node(preferred[0] if preferred else cards[0])
                time.sleep(7)
                self.wait_for('客服', min_y=760, timeout=12)
                return
            if time.monotonic() >= deadline:
                self.fail('商城搜索结果中未找到商品卡片')
            time.sleep(0.5)

    def add_current_product_to_cart(self):
        nodes = self.nodes()
        buttons = []
        for node in nodes:
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeOther'
                    and not self.node_name(node)
                    and 90 <= x <= 180 and y >= 770
                    and 80 <= width <= 120 and 40 <= height <= 70):
                buttons.append(node)
        if buttons:
            self.tap_node(buttons[0])
        else:
            # 2026-09-12 weditor（402×874）：商品详情底部首次加购按钮
            # 未提供 accessibility 名称，中心点为 (157, 813)。
            logging.warning('首次加购按钮未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(157, 813)
        time.sleep(4)
        self.tap('加入购物车', wait=6, timeout=10)

        nodes = self.nodes()
        prompt = self.find('请选择 ', contains=True, max_y=230, nodes=nodes)
        if prompt is not None:
            self._select_required_product_options(self.node_name(prompt), nodes)
            self.tap('加入购物车', min_y=760, wait=4, timeout=8)

        deadline = time.monotonic() + 10
        while True:
            nodes = self.nodes()
            if self.find('加入购物车成功', nodes=nodes) is not None:
                return
            # 部分商品只显示短暂 toast，随后直接收起规格面板；底部客服或
            # 带数量的购物车入口同样可以证明加购已完成。
            if self.find('客服', min_y=760, nodes=nodes) is not None:
                return
            carts = self.matching_nodes(
                '购物车', contains=True, min_y=740, nodes=nodes)
            if carts:
                return
            if time.monotonic() >= deadline:
                self.fail('点击加入购物车后未看到成功状态')
            time.sleep(0.5)

    def _select_required_product_options(self, prompt_text, nodes):
        required = [item.strip() for item in prompt_text.replace(
            '请选择 ', '', 1).split('/') if item.strip()]
        section_names = {
            '颜色', '版本', '成色', '机身颜色', '存储容量', '网络类型',
        }
        headers = []
        for node in nodes:
            name = self.node_name(node)
            if name in section_names:
                headers.append((float(node.get('y', 0)), name, node))
        headers.sort(key=lambda item: item[0])

        for index, (header_y, header_name, _) in enumerate(headers):
            if header_name not in required:
                continue
            next_y = (headers[index + 1][0]
                      if index + 1 < len(headers) else 780)
            choices = []
            for node in nodes:
                name = self.node_name(node)
                x, y, width, height = (float(node.get(key, 0))
                                       for key in ('x', 'y', 'width', 'height'))
                if (node.get('visible') == 'true'
                        and node.get('enabled') != 'false'
                        and header_y + 18 < y < next_y
                        and 20 <= x < 370 and 20 <= width <= 150
                        and 12 <= height <= 50
                        and name and name not in section_names
                        and name not in ('缺货', '小图', '查看全部')):
                    choices.append(node)
            if not choices:
                self.fail('商品规格“{}”没有可选项'.format(header_name))
            stock_markers = [node for node in nodes
                             if self.node_name(node) in ('缺货', '无货')]
            available = []
            for choice in choices:
                x = float(choice.get('x', 0))
                y = float(choice.get('y', 0))
                width = float(choice.get('width', 0))
                unavailable = any(
                    x - 8 <= float(marker.get('x', 0)) <= x + width + 8
                    and 0 <= y - float(marker.get('y', 0)) <= 30
                    for marker in stock_markers)
                if not unavailable:
                    available.append(choice)
            if available:
                choices = available
            choices.sort(key=lambda node: (
                float(node.get('y', 0)), float(node.get('x', 0))))
            self.tap_node(choices[0])
            time.sleep(1)
            nodes = self.nodes()

    def close_add_cart_panel(self):
        nodes = self.nodes()
        close = self.find('关闭', max_y=300, nodes=nodes)
        if close is not None:
            self.tap_node(close)
            time.sleep(3)
            return
        if self.find('客服', min_y=760, nodes=nodes) is not None:
            return
        if (self.find('加入购物车', min_y=760, nodes=nodes) is not None
                or self.find('已选择 ', contains=True,
                             max_y=230, nodes=nodes) is not None):
            # 2026-09-12 weditor（402×874）：部分商品规格面板右上角
            # “X”没有 accessibility 名称，中心点为 (375, 103)。
            self.device.click(375, 103)
            time.sleep(4)
            self.wait_for('客服', min_y=760, timeout=8)
            return
        self.fail('加购完成后未回到商品详情页')

    def open_customer_service(self):
        self.close_add_cart_panel()
        self.tap('客服', min_y=760, wait=6)
        self.wait_for('返回', max_y=130)

    def return_product_detail(self):
        self.tap('返回', max_y=130, wait=6)
        self.wait_for('客服', min_y=760, timeout=10)

    def enter_store(self):
        self.tap('进店', '店铺', min_y=760, wait=7)
        # 店铺页存在原生底栏和 Lynx 全屏页两种布局；两者分别暴露
        # “全部商品/商品分类”或“全部/分类”。
        self.wait_for('全部商品', '分类', contains=True, timeout=12)

    def return_mall_home(self):
        for _ in range(8):
            nodes = self.nodes()
            if self.find('我的订单', contains=True,
                         max_y=260, nodes=nodes) is not None:
                return
            back = self.find(
                '返回', '返回。按钮', '关闭,按钮', max_y=140, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            elif self.find('客服', min_y=760, nodes=nodes) is not None:
                # 部分二手商品详情页的左上角返回按钮没有 accessibility 名称。
                self.device.click(22, 84)
            else:
                self.device.swipe(0.01, 0.5, 0.88, 0.5, 0.3)
            time.sleep(3)
        self.fail('多次返回后仍未到达抖音商城首页')

    def open_mall_cart(self):
        nodes = self.nodes()
        carts = [node for node in self.matching_nodes(
            '购物车', contains=True, min_y=100, max_y=160, nodes=nodes)
                 if float(node.get('x', 0)) > 320]
        if not carts:
            self.fail('商城首页未找到右上角购物车')
        self.tap_node(carts[-1])
        time.sleep(6)
        self.wait_for('管理', max_y=130)

    def manage_cart(self):
        self.tap('管理', max_y=130, wait=3)
        self.wait_for('完成', max_y=130)

    def delete_selected_cart_items(self):
        self.tap('删除', contains=True, min_y=740, wait=4)

    def return_from_cart(self):
        self.tap('返回', max_y=130, wait=6)
        self.wait_for('我的订单', contains=True, max_y=260)

    def open_group_buy(self):
        self.select_top_channel('团购')

    def open_food(self):
        self.tap('附近美食', '美食', min_y=130, max_y=260, wait=7)
        self.wait_for('推荐', max_y=280, timeout=12)

    def open_first_food_merchant(self):
        candidates = []
        for node in self.nodes():
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and x >= 95 and 280 <= y < 780 and width >= 150
                    and 18 <= height <= 30):
                candidates.append(node)
        if not candidates:
            self.fail('美食列表中未找到可点击商家')
        candidates.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(candidates[0])
        time.sleep(7)
        self.wait_for('联系商家', timeout=12)

    def open_first_group_package(self):
        packages = [node for node in self.nodes()
                    if node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeButton'
                    and '抢购' in self.node_name(node)
                    and float(node.get('y', 0)) >= 450]
        if not packages:
            self.fail('商家页没有可购买的团购套餐')
        packages.sort(key=lambda node: float(node.get('y', 0)))
        self.tap_node(packages[0])
        time.sleep(7)
        self.wait_for('团购详情', timeout=12)

    def buy_current_group_package(self):
        nodes = self.nodes()
        button = self.find('购买', 'detail-pay-footer-content-button',
                           contains=True, min_y=740, nodes=nodes)
        if button is not None:
            self.tap_node(button)
        else:
            logging.warning('购买按钮未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(201, 819)
        time.sleep(6)

    def open_collection(self):
        self.tap('未选中, 收藏, 按钮', '已选中, 收藏, 仅自己可见, 按钮',
                 min_y=450, max_y=530, wait=5)
        self.wait_for('已选中, 收藏', contains=True, timeout=10)

    def open_likes(self):
        self.tap('未选中, 喜欢, 仅自己可见, 按钮',
                 '已选中, 喜欢, 仅自己可见, 按钮',
                 min_y=450, max_y=530, wait=5)
        self.wait_for('已选中, 喜欢', contains=True, timeout=10)

    def open_first_own_video(self):
        cards = self._profile_video_cards(self.nodes())
        if not cards:
            self.fail('当前收藏/喜欢列表没有可浏览作品')
        self.tap_node(cards[0])
        time.sleep(6)

    def return_to_me(self):
        # 作品持续播放时 XCTest 的 source 查询偶尔会永久等待，因此这里
        # 不先查树。2026-09-12 weditor（402×874）确认返回按钮命中区中心
        # 为 (28, 84)，点击后再在静态个人页进行结构校验。
        self.device.click(28, 84)
        time.sleep(5)
        self.wait_for('编辑主页', timeout=12)

    def open_wallet(self):
        self.tap('我的钱包', min_y=380, max_y=480, wait=7)

    def open_current_author(self):
        nodes = self.nodes()
        avatars = []
        for node in nodes:
            x, y, width, height = (float(node.get(key, 0))
                                   for key in ('x', 'y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeOther'
                    and self.node_name(node) not in ('', '圆角遮罩')
                    and x >= 330 and 300 <= y <= 470
                    and 35 <= width <= 70 and 50 <= height <= 90):
                avatars.append(node)
        if avatars:
            self.tap_node(avatars[0])
        else:
            author_links = [node for node in nodes
                            if node.get('visible') == 'true'
                            and node.tag == 'XCUIElementTypeButton'
                            and self.node_name(node).startswith('@')
                            and 550 <= float(node.get('y', 0)) <= 790]
            if author_links:
                self.tap_node(author_links[0])
            else:
                top_authors = [node for node in nodes
                               if node.get('visible') == 'true'
                               and node.tag == 'XCUIElementTypeButton'
                               and self.node_name(node) not in {
                                   '关注', '返回', '更多', '搜索', '取消静音'}
                               and 50 <= float(node.get('x', 0)) <= 290
                               and 55 <= float(node.get('y', 0)) <= 115
                               and float(node.get('width', 0)) >= 80]
                if top_authors:
                    self.tap_node(top_authors[0])
                else:
                    # 2026-09-12 weditor（402×874）：推荐视频右侧作者头像中心。
                    logging.warning('作者头像未暴露给 WDA，使用 weditor 核对坐标')
                    self.device.click(373, 395)
        time.sleep(5)
        nodes = self.nodes()
        if self.find('作品', contains=True, min_y=420, nodes=nodes) is None:
            # 图文推荐点击头像区域后可能先进入作品详情；此时作者名称位于
            # 顶栏中部，点击它可继续进入同一个 UP 主主页。
            top_authors = []
            ignored = {'关注', '返回', '更多', '搜索', '取消静音'}
            for node in nodes:
                name = self.node_name(node)
                x, y, width = (float(node.get(key, 0))
                               for key in ('x', 'y', 'width'))
                if (node.get('visible') == 'true'
                        and node.tag == 'XCUIElementTypeButton'
                        and name not in ignored and 50 <= x <= 290
                        and 55 <= y <= 115 and width >= 80):
                    top_authors.append(node)
            if not top_authors:
                self.fail('推荐内容未暴露可点击的 UP 主入口')
            self.tap_node(top_authors[0])
            time.sleep(6)
        self.wait_for('作品', contains=True, min_y=420, timeout=12)

    def open_me(self):
        self.tap('我', min_y=740, wait=6)
        self.wait_for('编辑主页', timeout=10)

    def open_following(self):
        self.tap('关注', min_y=260, max_y=340, wait=6)
        self.wait_for('搜索用户备注或名字', timeout=10)

    def open_followed_profile(self, creator):
        self.tap(creator, min_y=320, wait=7)
        self.wait_for('作品', contains=True, min_y=450, timeout=12)

    def _profile_video_cards(self, nodes):
        cards = []
        for node in nodes:
            name = self.node_name(node)
            y, width, height = (float(node.get(key, 0))
                                for key in ('y', 'width', 'height'))
            if (node.get('visible') == 'true'
                    and node.tag in ('XCUIElementTypeOther', 'XCUIElementTypeCell')
                    and '视频,' in name and '直播中' not in name
                    and y >= 500 and 110 <= width <= 150 and height >= 130):
                cards.append(node)
        return sorted(cards, key=lambda node: (
            float(node.get('y', 0)), float(node.get('x', 0))))

    def _ensure_profile_top(self):
        for _ in range(7):
            nodes = self.nodes()
            cards = self._profile_video_cards(nodes)
            if (self.find('获赞', max_y=350, nodes=nodes) is not None
                    and cards):
                return nodes
            self.swipe_down_times(1, pause=1)
        self.fail('未能回到 UP 主主页顶部')

    def open_profile_video(self, number):
        nodes = self._ensure_profile_top()
        cards = self._profile_video_cards(nodes)
        if len(cards) < number:
            self.fail('UP 主主页可识别的视频不足{}个'.format(number))
        target_name = self.node_name(cards[number - 1])
        target = cards[number - 1]
        center_y = (float(target.get('y', 0))
                    + float(target.get('height', 0)) / 2)
        if center_y > 790:
            self.device.swipe(0.5, 0.78, 0.5, 0.55, 0.3)
            time.sleep(2)
            matches = self.matching_nodes(target_name)
            if not matches:
                self.fail('滚动后未找到第{}个视频'.format(number))
            target = matches[0]
        self.tap_node(target)
        time.sleep(6)
        # 和抖音极速版相同，持续播放页会让 WDA 拉取 source 长时间无响应；
        # 进入后不再读取页面树，按模型停留时长后直接执行返回手势。

    def return_to_profile(self):
        # 视频页可能让 XCTest 的窗口/页面树查询一直等待。这里必须使用
        # 绝对坐标；比例坐标会让 facebook-wda 先调用 window_size()。
        self.device.swipe(4, 437, 354, 437, 0.3)
        time.sleep(4)
        # 不在视频页立即读取 source；下一次主页操作再做结构化定位。

    def search_creator(self, creator):
        self.return_main()
        self.tap('aweme.feed.top_bar.search_entry', max_y=130, wait=3)
        self.wait_for('aweme.search.search_bar.input', timeout=8)
        self.enter_text(creator, clear=True)
        self.tap('搜索', max_y=130, wait=7)
        self.wait_for(creator, contains=True, min_y=190, max_y=420,
                      timeout=12)

    def open_search_creator_profile(self, creator):
        nodes = self.nodes()
        candidates = []
        for node in nodes:
            name = self.node_name(node)
            x, y, width = (float(node.get(key, 0))
                           for key in ('x', 'y', 'width'))
            if (node.get('visible') == 'true' and creator in name
                    and 190 <= y <= 400 and width >= 180
                    and ('粉丝' in name or x >= 70)):
                candidates.append(node)
        if candidates:
            candidates.sort(key=lambda node: (
                float(node.get('y', 0)), -float(node.get('width', 0))))
            self.tap_node(candidates[0])
        else:
            # 搜索用户卡片由 Lynx 绘制时，正文稳定占据首个用户结果右侧。
            logging.warning('搜索用户卡片未暴露给 WDA，使用 weditor 核对坐标')
            self.device.click(190, 280)
        time.sleep(7)
        self.wait_for('作品', contains=True, min_y=420, timeout=12)
