"""WPS Office 动态性能用例的 WDA 页面能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class WpsOfficeCase(WdaCase):
    PACKAGE = 'com.kingsoft.www.office.wpsoffice'
    APP_NAME = 'WPS Office'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def _enable_continuous_ui_mode(self):
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
            logging.exception('设置 WPS 连续页面模式失败')

    def _restore_idle_settings(self):
        settings = getattr(self, '_previous_idle_settings', None)
        if settings is not None:
            try:
                self.device.appium_settings(settings)
            except Exception:
                logging.exception('恢复 WDA idle 设置失败')
        self._previous_idle_settings = None

    def prepare_iteration(self):
        self._enable_continuous_ui_mode()
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束 WPS 进程失败，继续尝试启动')
        time.sleep(1)

    def launcher(self):
        try:
            super().launcher()
        finally:
            self._restore_idle_settings()

    def dismiss_optional_prompts(self):
        """关闭广告、升级、权限和恢复文档提示，不触碰购买按钮。"""
        for _ in range(8):
            try:
                alert = self.device.alert
                buttons = alert.buttons()
                if buttons:
                    if '不允许' in buttons:
                        alert.click('不允许')
                    elif '取消' in buttons:
                        alert.click('取消')
                    else:
                        alert.dismiss()
                    time.sleep(2)
                    continue
            except Exception:
                pass
            nodes = self.nodes()
            button = self.find(
                '关闭', '取消', '以后再说', '暂不升级', '稍后再说',
                '暂不开启', '我知道了', '跳过', nodes=nodes)
            if button is None:
                return
            self.tap_node(button)
            time.sleep(2)

    def _is_home(self, nodes=None):
        nodes = self.nodes() if nodes is None else nodes
        return (self.find('首页', min_y=740, nodes=nodes) is not None
                and self.find('云盘', '云文档', min_y=740, nodes=nodes) is not None
                and self.find('我', min_y=740, nodes=nodes) is not None)

    def return_home(self):
        for _ in range(10):
            self.dismiss_optional_prompts()
            nodes = self.nodes()
            if self._is_home(nodes):
                self.tap_node(self.find('首页', min_y=740, nodes=nodes))
                time.sleep(3)
                return
            if self.find('空白文档', max_y=220, nodes=nodes) is not None:
                # 文字模板页的左上返回箭头没有可访问名称。
                self.device.click(25, 96)
                time.sleep(3)
                continue
            back = self.find('返回', 'arrow left l 22', 'pub nav back', 'nav back',
                             max_y=160, nodes=nodes)
            if back is not None:
                self.tap_node(back)
            else:
                self.device.swipe_right()
            time.sleep(3)
        self.fail('多次返回后仍未到达 WPS 首页')

    def start_wps(self):
        self.start_app(wait=7)
        self.dismiss_optional_prompts()
        self.return_home()

    def browse_horizontal(self, left=5, right=5):
        for start, end, count in ((0.78, 0.25, left), (0.25, 0.78, right)):
            for _ in range(count):
                self.device.swipe(start, 0.5, end, 0.5, 0.3)
                time.sleep(1)

    def switch_cloud_home(self, repeats=5):
        for _ in range(repeats):
            self.tap('云盘', '云文档', min_y=740, wait=2)
            self.tap('首页', min_y=740, wait=2)

    def open_my(self):
        self.tap('我', min_y=740, wait=5)

    def _scroll_personal_center(self):
        # WPS 的“我”页会吞掉慢速 drag；WDA 的快速抛滑可以稳定滚动。
        self.device.swipe_up()
        time.sleep(2)
        self.device.swipe_up()
        time.sleep(3)

    def _tap_personal_row(self, accessibility_name):
        """WPS 会把已显示行标成 visible=false，直接按元素实际 frame 点整行。"""
        try:
            element = self.device(name=accessibility_name).get(timeout=3)
        except Exception:
            self.fail('“我”页面未找到入口：{}'.format(accessibility_name))
        bounds = element.bounds
        if not 110 <= bounds.y + bounds.height / 2 <= 760:
            self.fail('入口“{}”未滚动到可点击区域'.format(accessibility_name))
        self.device.click(200, round(bounds.y + bounds.height / 2))
        time.sleep(5)

    def open_settings(self):
        self._scroll_personal_center()
        self._tap_personal_row('sidebar_setting3')
        if self.find('设置', max_y=160) is None:
            self.fail('点击设置入口后未进入设置页')

    def back_to_my(self):
        back = self.find('返回', 'arrow left l 22', 'pub nav back', max_y=160)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
        time.sleep(5)

    def open_super_member(self):
        # 设置页返回时列表仍在下方；先回到顶部再点“超级会员”。
        self.device.swipe_down()
        time.sleep(2)
        self.device.swipe_down()
        time.sleep(3)
        self._tap_personal_row('超级会员')
        if self.find('会员支付', contains=True) is None:
            self.fail('点击超级会员后未进入会员支付页')

    def back_from_member(self):
        back = self.find('返回', 'arrow left l 22', 'pub nav back', 'nav back',
                         max_y=160)
        if back is not None:
            self.tap_node(back)
        else:
            # 会员 H5 当前只绘制左上角箭头，不暴露可访问名称。
            self.device.click(28, 88)
        time.sleep(5)

    def open_welcome_document(self):
        self.tap('欢迎使用WPS云文档', contains=True, wait=7)

    def browse_document(self, up=5, down=5):
        self.browse(up, down)

    def back_from_document(self):
        back = self.find('返回', 'arrow left l 22', max_y=160)
        if back is not None:
            self.tap_node(back)
        else:
            self.device.swipe(0.02, 0.5, 0.82, 0.5, 0.25)
        time.sleep(5)

    def open_docer(self):
        self.tap('稻壳儿', min_y=740, wait=7)

    def open_new_menu(self):
        self.tap('新建', min_y=650, wait=4)

    def create_blank_word(self):
        self.tap('文字', contains=True, wait=6)
        self.tap('空白文档', contains=True, wait=7)
        if self.find('保存', max_y=170) is None:
            self.fail('新建空白文字后未进入编辑器')

    def input_document_text(self, text):
        text_view = self.find('opened')
        if text_view is not None:
            self.tap_node(text_view)
            time.sleep(1)
        self.enter_text(text, clear=False)
        time.sleep(2)

    def open_save_as(self):
        self.tap('保存', max_y=170, wait=5)
        if self.find('更改路径', contains=True) is None:
            self.fail('点击保存后未进入另存为页面')

    def open_local_save_location(self):
        self.tap('更改路径', contains=True, wait=4)
        self.tap('本机', '本地文件夹', contains=True, wait=5)

    def choose_document_folder(self):
        folder = self.find('文档', contains=True)
        if folder is None:
            self.tap('新建文件夹', contains=True, wait=2)
            self.enter_text('文档', clear=True)
            self.tap('确认', wait=5)
            folder = self.find('文档', contains=True)
        if folder is None:
            self.fail('本机目录中无法创建或找到“文档”文件夹')
        self.tap_node(folder)
        time.sleep(4)

    def confirm_path_and_save(self):
        self.tap('确定', wait=5)
        if self.find('保存') is None:
            self.fail('选择本机“文档”文件夹后未返回另存为页面')
        # 不能用 contains=True，否则会误点上方“保存路径”文本。
        self.tap('保存', wait=7)
        # 重复执行时 WPS 弹出“替换文件 / 创建副本 / 取消”。创建副本既不
        # 覆盖旧文档，又能保持用例每轮都完成保存，文件名由 WPS 自动加后缀。
        if self.find('当前位置存在同名文件', contains=True) is not None:
            create_copy = self.find('创建副本')
            if create_copy is None:
                self.fail('出现同名文件提示，但未找到“创建副本”按钮')
            self.tap_node(create_copy)
            time.sleep(7)
        if self.find('当前位置存在同名文件', contains=True) is not None:
            self.fail('选择“创建副本”后同名文件提示仍未关闭')
        if self.find('arrow left l 22', max_y=160) is None:
            self.fail('保存后未返回文档编辑页面')

    def open_created_document(self):
        target = self.find('动态性能测试', contains=True)
        if target is None:
            cells = [node for node in self.nodes()
                     if node.get('visible') == 'true'
                     and node.tag == 'XCUIElementTypeCell'
                     and 120 <= float(node.get('y', 0)) < 720]
            if not cells:
                self.fail('WPS 首页文件列表中没有可浏览的文档')
            cells.sort(key=lambda node: float(node.get('y', 0)))
            target = cells[0]
        self.tap_node(target)
        time.sleep(7)
