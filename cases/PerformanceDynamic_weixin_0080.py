import logging

from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0080(WeixinCase):
    """Excel 7.0.2：好友聊天拍照与录像。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击测试账号，进入好友聊天页')
            self.open_chat(self.TEST_ACCOUNT)
            self.step(3, '点击加号，进入更多功能页')
            self.open_chat_actions()
            self.step(4, '点击拍摄，进入相机')
            self.open_chat_camera()
            self.step(5, '点击拍照按钮')
            self.tap('拍照', min_y=650, wait=3)
            self.step(6, '点击发送，返回聊天页')
            self.tap('发送', min_y=650, wait=4)
            self.step(7, '点击加号，进入更多功能页')
            self.open_chat_actions()
            self.step(8, '点击拍摄，进入相机')
            self.open_chat_camera()
            self.step(9, '确认录像模式（新版微信改为长按快门）')
            self.wait_for('拍照', min_y=650, timeout=5)
            logging.warning('当前微信无单独“录像”按钮，使用长按快门的等价操作')
            self.step(10, '长按快门开始录像')
            self.start_chat_video_recording(duration=4)
            self.step(11, '松开快门停止录像')
            self.stop_chat_video_recording()
            self.step(12, '点击发送，返回聊天页')
            self.tap('发送', min_y=650, wait=5)
            self.step(13, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
