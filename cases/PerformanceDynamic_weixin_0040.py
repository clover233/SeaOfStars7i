from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0040(WeixinCase):
    """Excel 7.0.2：文字、语音、表情及音视频通话。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击测试账号，进入好友聊天页面')
            self.open_chat(self.TEST_ACCOUNT)
            self.step(3, '点击输入框，进入消息编辑界面')
            self.tap_chat_input()
            self.step(4, '输入哈哈哈，点击发送')
            self.device.send_keys('哈哈哈')
            self.tap('Send', '发送', min_y=700, wait=3)
            self.step(5, '点击语音按钮，发送语音给好友')
            self.send_voice_message()
            self.step(6, '点击表情包按钮，进入表情框界面')
            self.tap('表情', min_y=400, wait=1)
            self.step(7, '点击选择前三个表情，点击发送')
            for name in ('微笑', '撇嘴', '色'):
                self.tap(name, min_y=540, wait=0.4)
            self.tap('发送', min_y=700, wait=3)
            self.step(8, '点击加号按钮，进入更多功能页面')
            self.tap('更多', min_y=400, choose='last', wait=1)
            self.step(9, '点击视频通话，进入选择通话界面')
            self.tap('视频通话', min_y=500, wait=1)
            self.step(10, '点击视频通话，进入视频通话界面')
            self.tap('视频通话', min_y=620, wait=4)
            self.step(11, '点击挂断按钮，返回好友聊天页面')
            hangup = self.find('挂断', '结束通话', contains=True)
            if hangup is None:
                self.fail('视频通话界面未找到挂断按钮，请检查相机/麦克风权限')
            self.tap_node(hangup)
            self.return_weixin_chat()
            self.step(12, '点击加号按钮，进入更多功能页面')
            self.tap('更多', min_y=400, choose='last', wait=1)
            self.step(13, '点击视频通话，进入选择通话界面')
            self.tap('视频通话', min_y=500, wait=1)
            self.step(14, '点击语音通话，进入语音通话界面')
            self.tap('语音通话', min_y=620, wait=4)
            self.step(15, '点击挂断按钮，返回好友聊天页面')
            hangup = self.find('挂断', '结束通话', contains=True)
            if hangup is None:
                self.fail('语音通话界面未找到挂断按钮，请检查麦克风权限')
            self.tap_node(hangup)
            self.return_weixin_chat()
            self.step(16, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 17):
                self.step(17, '滑动返回Home页')
                self.launcher()
