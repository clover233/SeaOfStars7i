import logging
import time

from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0040(DouyinCase):
    """Excel 7.0.2：浏览推荐视频作者和华为终端 UP 主主页。"""

    def _browse_current_author_once(self):
        self.swipe_up_times(5)
        self.open_current_author()
        self.return_main()

    def _search_creator_once(self):
        self.search_creator('华为终端')
        self.open_search_creator_profile('华为终端')
        self.browse(3, 3)
        self.return_main()

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动抖音')
                self.start_douyin()
            self.step(2, '推荐页面上滑切换视频，重复5次')
            self.swipe_up_times(5)
            self.step(3, '点击当前视频的UP主头像进入UP主主页')
            self.open_current_author()
            self.step(4, '返回抖音主界面，步骤2至4重复1次')
            self.return_main()
            self._browse_current_author_once()
            self.step(5, '点击我，切换到我页面')
            self.open_me()
            self.step(6, '点击关注，切换到关注页面')
            self.open_following()
            self.step(7, '点击华为终端头像查看博主主页信息')
            self.open_followed_profile('华为终端')
            self.step(8, '博主主页上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '点击播放博主的第1个视频，浏览15s')
            self.open_profile_video(1)
            time.sleep(15)
            self.step(10, '左滑返回博主主页')
            self.return_to_profile()
            self.step(11, '点击播放第2个视频，浏览15s')
            self.open_profile_video(2)
            time.sleep(15)
            self.step(12, '左滑返回博主主页')
            self.return_to_profile()
            self.step(13, '点击播放第3个视频，浏览15s')
            self.open_profile_video(3)
            time.sleep(15)
            self.step(14, '左滑返回博主主页')
            self.return_to_profile()
            self.step(15, '返回抖音主界面')
            self.return_main()
            self.step(16, '点击搜索框，搜索华为终端')
            self.search_creator('华为终端')
            self.step(17, '点击搜索结果中当前视频的UP主头像进入UP主页')
            self.open_search_creator_profile('华为终端')
            self.step(18, 'UP主主页上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(19, '返回抖音主界面，步骤16至19重复执行3次')
            self.return_main()
            # Excel 的“重复执行3次”按整组总计3轮处理，首轮已在上方完成。
            for repeat_index in range(2):
                logging.info('执行搜索UP主流程第%d/3轮', repeat_index + 2)
                self._search_creator_once()
            with self.capture_trace(iteration, 20):
                self.step(20, '滑动返回Home页')
                self.launcher()
