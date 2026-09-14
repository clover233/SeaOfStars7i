import time

from aw import SeaOfStarsAW
from cases.qq_common import QqCase


class PerformanceDynamic_qq_0020(QqCase):
    """Excel 7.0.2：浏览群图片并发送文字、表情和图片。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动QQ')
                self.start_qq()
            self.step(2, '点击【测试图片群】，查看群聊消息')
            self.open_chat_from_message_list('测试图片群', '图片测试群')
            self.step(3, '好友群浏览消息，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(4, '点击群聊中的图片，查看大图，右滑4次，左滑4次')
            self.open_picture_message()
            self.swipe_images(4, 4)
            self.step(5, '侧滑返回消息列表界面')
            self.return_to_message_list()
            self.step(6, '点击多媒体消息的聊天群')
            self.open_chat_from_message_list('多媒体消息')
            self.step(7, '发送文字你好，动态')
            self.send_text_message('你好，动态')
            self.step(8, '发送表情')
            self.send_classic_emoji()
            self.step(9, '发送图片')
            self.send_first_photo()
            self.step(10, '侧滑返回消息页')
            self.return_to_message_list()
            with self.capture_trace(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
