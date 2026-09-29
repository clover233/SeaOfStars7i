from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0010(WeixinCase):
    """Excel 7.0.2：微信聊天图片、视频转发及语音播放。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击性能图片群，进入群聊界面')
            self.open_chat(self.IMAGE_GROUP)
            self.step(3, '点击一张图片，向右滑动3次向左滑动3次浏览图片页面')
            self.open_chat_media('图片')
            self.horizontal_browse(3, 3)
            self.step(4, '返回微信主界面')
            self.return_weixin_home()
            self.step(5, '点击性能测试群，进入群聊界面')
            self.open_chat(self.VIDEO_GROUP)
            self.step(6, '点击一个视频，向右滑动3次向左滑动3次')
            self.open_chat_media('视频')
            self.horizontal_browse(3, 3)
            self.step(7, '长按视频，进入待转发视频页面')
            self.long_press_current_media()
            self.step(8, '点击转发给朋友，进入转发视频界面')
            self.tap('转发给朋友', wait=3)
            self.step(9, '点击测试，进入确认发送界面')
            self.select_forward_recipient('测试')
            self.step(10, '点击发送，完成发送并进入查看视频界面')
            self.tap('发送', min_y=700, wait=3)
            self.step(11, '返回微信主界面')
            self.return_weixin_home()
            self.step(12, '点击性能测试语音群，进入群聊界面')
            self.open_chat(self.VOICE_GROUP, self.VOICE_GROUP + '群')
            self.step(13, '点击一个语音进行播放')
            self.play_first_voice()
            self.step(14, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
