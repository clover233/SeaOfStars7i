import time

from aw import SeaOfStarsAW
from cases.bilibili_common import BilibiliCase


class PerformanceDynamic_bilibili_0030(BilibiliCase):
    """Excel 7.0.2：播放视频、发送弹幕并浏览评论。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动哔哩哔哩')
                self.start_bilibili()
            self.step(2, '点击热门')
            self.open_channel('热门')
            self.step(3, '上滑5次浏览热门页面')
            self.browse(5, 0)
            self.step(4, '下滑5次浏览热门页面')
            self.browse(0, 5)
            self.step(5, '点击某一个视频播放')
            self.open_first_hot_video()
            self.step(6, '点击屏幕调出菜单键，点击全屏按钮')
            self.enter_full_screen()
            self.step(7, '观看10秒视频')
            time.sleep(10)
            self.step(8, '双击暂停视频往弹幕框输入还行')
            self.type_barrage('还行')
            self.step(9, '点击发送弹幕')
            self.send_barrage()
            self.step(10, '双击屏幕继续观看5秒视频')
            self.resume_video(5)
            self.step(11, '侧滑退出全屏')
            self.exit_full_screen()
            self.step(12, '点击评论')
            self.open_comments()
            self.step(13, '上滑5次浏览评论页面')
            self.browse(5, 0)
            self.step(14, '下滑5次浏览评论页面')
            self.browse(0, 5)
            self.step(15, '返回哔哩哔哩主界面')
            self.return_bilibili_home()
            with self.capture_trace(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
