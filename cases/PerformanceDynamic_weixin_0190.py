from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0190(WeixinCase):
    """Excel 7.0.2：微信选择多张照片并打开大图。"""

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
            self.step(3, '点击加号按钮，进入更多功能页面')
            self.open_chat_actions()
            self.step(4, '点击照片，进入照片页面')
            self.open_photo_picker()
            self.step(5, '浏览照片页面，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(6, '点击选择多张图片')
            self.select_photos(3)
            self.step(7, '点击发送，进入好友聊天页面')
            self.tap('发送(3)', '发送', contains=True, min_y=760, wait=5)
            self.step(8, '点击加号按钮，进入更多功能页面')
            self.open_chat_actions()
            self.step(9, '点击照片，进入照片页面')
            self.open_photo_picker()
            self.step(10, '点击第一张图片大图，进入大图界面')
            self.open_first_photo_preview()
            self.step(11, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
