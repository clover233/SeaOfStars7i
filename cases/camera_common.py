"""iOS 相机动态性能用例的 WDA 页面能力。"""

import logging
import re
import time

from cases.wda_case_common import WdaCase


class CameraCase(WdaCase):
    PACKAGE = 'com.apple.camera'
    APP_NAME = '相机'

    def start_camera(self):
        self.start_app(wait=4)
        if self.find('PhotoCapture', 'VideoCapture') is None:
            self.fail('相机预览页未加载')

    def ensure_photo_mode(self):
        if self.find('PhotoCapture') is None:
            if self.find('PhotoModeButton') is not None:
                self.tap('PhotoModeButton', wait=2)
            else:
                size = self.device.window_size()
                for _ in range(6):
                    if self.find('PhotoCapture') is not None:
                        break
                    self.device.click(round(size.width * 0.63),
                                      round(size.height * 0.795))
                    time.sleep(1)
        if self.find('PhotoCapture') is None:
            self.fail('无法切换到拍照模式')

    def ensure_video_mode(self):
        if self.find('VideoCapture') is None:
            if self.find('VideoModeButton') is not None:
                self.tap('VideoModeButton', wait=2)
            else:
                size = self.device.window_size()
                for _ in range(6):
                    if self.find('VideoCapture') is not None:
                        break
                    self.device.click(round(size.width * 0.37),
                                      round(size.height * 0.795))
                    time.sleep(1)
        if self.find('VideoCapture') is None:
            self.fail('无法切换到录像模式')

    def _zoom_nodes(self):
        result = []
        for node in self.nodes():
            if (node.get('visible') == 'true'
                    and node.tag == 'XCUIElementTypeStaticText'
                    and 400 < float(node.get('y', 0)) < 700
                    and float(node.get('height', 0)) >= 25):
                name = self.node_name(node)
                if re.fullmatch(r'\.?\d+(?:\.\d+)?(?:×)?', name):
                    result.append(node)
        return result

    def set_zoom(self, *labels):
        candidates = []
        for node in self._zoom_nodes():
            if self.node_name(node) in labels:
                candidates.append(node)
        if not candidates:
            self.fail('未找到相机焦段：{}'.format(' / '.join(labels)))
        candidates.sort(key=lambda node: float(node.get('x', 0)))
        self.tap_node(candidates[0])
        time.sleep(1)

    def set_wide_zoom(self):
        self.set_zoom('.5', '.5×', 'W')

    def set_one_x(self):
        self.set_zoom('1×', '1')

    def set_two_x(self):
        self.set_zoom('2×', '2')

    def set_max_zoom(self):
        self.set_two_x()
        window = self.device(type='XCUIElementTypeWindow')
        for _ in range(4):
            window.pinch(2.0, 1.0)
            time.sleep(0.4)
        values = []
        for node in self._zoom_nodes():
            name = self.node_name(node).replace('×', '')
            try:
                values.append(float(name))
            except ValueError:
                pass
        if values:
            logging.info('已调整到设备当前最高可用倍数：%sX', max(values))

    def capture_photo(self, count=1, focus=False):
        self.ensure_photo_mode()
        if focus:
            size = self.device.window_size()
            self.device.click(round(size.width / 2), round(size.height * 0.42))
            time.sleep(1)
        for _ in range(count):
            self.tap('PhotoCapture', wait=1)

    def open_controls(self):
        if self.find('相机控制') is None:
            self.tap('ControlPanelToggleButton', wait=2)

    def close_controls(self):
        if self.find('相机控制') is not None:
            size = self.device.window_size()
            self.device.click(round(size.width / 2), round(size.height * 0.35))
            time.sleep(1)

    def open_settings_or_skip(self):
        nodes = self.nodes()
        settings = self.find('设置', contains=True, nodes=nodes)
        if settings is None:
            logging.warning('原生 iPhone 相机没有相机内“设置”入口，跳过该功能')
            return False
        self.tap_node(settings)
        time.sleep(2)
        return True

    def browse_settings_or_controls(self):
        logging.warning('原生相机无独立设置页，改为浏览已展开的相机控制面板')
        self.open_controls()
        for _ in range(3):
            self.browse(1, 1)

    def open_aspect_ratio(self):
        self.open_controls()
        nodes = self.nodes()
        control = self.find('AspectRatioButton', nodes=nodes)
        if control is None:
            logging.warning('当前相机没有宽高比控件，跳过照片比例')
            return False
        self.tap_node(control)
        time.sleep(1)
        return True

    def close_aspect_ratio(self):
        logging.warning('iPhone 宽高比不是弹框，点击取景器关闭控制面板')
        self.close_controls()

    @staticmethod
    def skip_unsupported(feature):
        logging.warning('原生 iPhone 相机不具备“%s”，按用例要求跳过', feature)

    def try_xiaoyi_vision(self):
        nodes = self.nodes()
        button = self.find('小艺视觉', '小艺', '扫一扫', contains=True, nodes=nodes)
        if button is None:
            self.skip_unsupported('小艺视觉')
            return False
        self.tap_node(button)
        time.sleep(2)
        return True

    def open_recent_media(self):
        self.tap('GoToCameraRoll', wait=3)
        for _ in range(8):
            nodes = self.nodes()
            # iOS 新旧图库分别暴露“完成”或关闭控件；全屏预览可能
            # 隐藏工具栏，此时相机快门消失也表示已经进入最近项目。
            if (self.find('PUOneUpBarButtonItemIdentifierDone', 'BackButton',
                          '完成', '关闭', '返回相机', nodes=nodes) is not None
                    or (self.find('GoToCameraRoll', nodes=nodes) is None
                        and self.find('PhotoCapture', 'VideoCapture',
                                      nodes=nodes) is None)):
                return
            time.sleep(0.5)
        self.fail('未打开最近拍摄内容')

    def swipe_media_left(self, count):
        for _ in range(count):
            self.device.swipe(0.85, 0.5, 0.15, 0.5, 0.3)
            time.sleep(0.5)

    def return_from_recent_media(self):
        for _ in range(3):
            if self.find('PhotoCapture', 'VideoCapture') is not None:
                return
            close = self.find('PUOneUpBarButtonItemIdentifierDone',
                              'BackButton', '完成', '关闭', '返回相机',
                              max_y=180)
            if close is not None:
                self.tap_node(close)
            else:
                # 视频播放时单击只显示隐藏的工具栏，第二次才会返回。
                self.device.click(30, 70)
            time.sleep(2)
        if self.find('PhotoCapture', 'VideoCapture') is None:
            self.fail('浏览最近拍摄内容后未返回相机')

    def open_photo_library(self):
        self.open_recent_media()
        if self.find('PUOneUpBarButtonItemIdentifierAllPhotos') is not None:
            self.tap('PUOneUpBarButtonItemIdentifierAllPhotos', wait=3)
        else:
            logging.warning('最近项目页没有“所有照片”入口，继续使用当前图库页')

    def return_from_photo_library(self):
        # “所有照片”会切换到照片 App，WDA 侧滑无法回到相机，重新激活相机等价返回。
        self.device.app_activate(self.PACKAGE)
        time.sleep(3)

    def flip_camera(self):
        self.tap('FlipButton', 'FrontBackFacingCameraChooser', wait=2)

    def set_video_format(self, fps):
        self.ensure_video_mode()
        if self.find('帧速率') is not None:
            # iOS 17 相机直接点顶部“高清/帧速率”循环切换，当前值在
            # 控件 value 中；无需打开 iOS 26 的视频格式菜单。
            for _ in range(4):
                nodes = self.nodes()
                resolution = self.find('分辨率', nodes=nodes)
                if resolution is not None and resolution.get('value') != '高清':
                    self.tap_node(resolution)
                    time.sleep(1)
                    continue
                rate = self.find('帧速率', nodes=nodes)
                if rate is not None and str(fps) in rate.get('value', ''):
                    return
                if rate is not None:
                    self.tap_node(rate)
                    time.sleep(1)
            self.fail('未设置为1080p{}fps'.format(fps))
        self.tap('VideoFrameRateButton', wait=1)
        self.tap('分辨率高清Button', wait=1)
        self.tap('帧速率{}Button'.format(fps), wait=1)
        size = self.device.window_size()
        self.device.click(round(size.width / 2), round(size.height * 0.35))
        time.sleep(1)
        nodes = self.nodes()
        if self.find(str(fps), max_y=130, nodes=nodes) is None:
            self.fail('未设置为1080p{}fps'.format(fps))

    def record_video(self, seconds):
        self.ensure_video_mode()
        self.tap('VideoCapture', wait=1)
        time.sleep(seconds)
        self.tap('VideoCapture', wait=2)

    def play_recent_video(self):
        size = self.device.window_size()
        self.device.click(round(size.width / 2), round(size.height / 2))
        time.sleep(0.5)
        if self.find('OneUpPlayButton') is not None:
            self.tap('OneUpPlayButton', wait=2)
        else:
            logging.warning('最近视频已自动播放，未显示独立播放按钮')

    def return_to_photo_by_swipe(self):
        size = self.device.window_size()
        self.device.swipe(round(size.width * 0.2), round(size.height * 0.45),
                          round(size.width * 0.8), round(size.height * 0.45), 0.3)
        time.sleep(2)
        if self.find('PhotoCapture') is None and self.find('PhotoModeButton') is None:
            self.ensure_photo_mode()
            return
        # iOS 26 中录像右滑会经过“电影效果/慢动作”；继续遍历模式直到照片。
        for _ in range(5):
            if self.find('PhotoCapture') is not None:
                return
            if self.find('PhotoModeButton') is not None:
                self.tap('PhotoModeButton', wait=2)
                continue
            if self.find('VideoModeButton') is not None:
                self.tap('VideoModeButton', wait=2)
                continue
            self.device.swipe(round(size.width * 0.8), round(size.height * 0.45),
                              round(size.width * 0.2), round(size.height * 0.45), 0.3)
            time.sleep(2)
        self.fail('右滑并遍历相机模式后仍未进入拍照界面')

    def invoke_siri_for_camera_advice(self, query):
        nodes = self.nodes()
        ai_button = self.find('小艺', 'AI', contains=True, nodes=nodes)
        if ai_button is not None:
            self.tap_node(ai_button)
            time.sleep(1)
            self.enter_text(query, clear=True)
            self.tap('发送', wait=2)
            return
        logging.warning('原生 iPhone 相机没有 AI 条，使用 WDA Siri 指令作为替代')
        try:
            self.device.siri_activate(query)
        except Exception as error:
            logging.warning('Siri 调用不可用，跳过相机建议问答：%s', error)

    def close_ai_or_siri(self):
        nodes = self.nodes()
        close = self.find('关闭', '取消', 'X', nodes=nodes)
        if close is not None:
            self.tap_node(close)
            time.sleep(1)
        self.device.app_activate(self.PACKAGE)
        time.sleep(2)
