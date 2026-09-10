import time

from aw import SeaOfStarsAW
from cases.bilibili_common import BilibiliCase


class PerformanceDynamic_bilibili_0040(BilibiliCase):
    """Excel 7.0.2：搜索“华为终端”并浏览视频和UP主主页。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动哔哩哔哩')
                self.start_bilibili()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '输入华为终端后，点击搜索按钮')
            self.search('华为终端')
            self.step(4, '上滑5次浏览搜索结果页面')
            self.browse(5, 0)
            self.step(5, '下滑5次浏览搜索结果页面')
            self.browse(0, 5)
            self.step(6, '点击其中一个视频播放')
            self.open_search_result_video()
            self.step(7, '观看视频10秒')
            time.sleep(10)
            self.step(8, '点击UP头像进入主页')
            self.open_up_profile()
            self.step(9, '上滑5次UP主页页面')
            self.browse(5, 0)
            self.step(10, '下滑5次UP主页页面')
            self.browse(0, 5)
            self.step(11, '返回哔哩哔哩主界面')
            self.return_bilibili_home()
            with self.capture_trace(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
