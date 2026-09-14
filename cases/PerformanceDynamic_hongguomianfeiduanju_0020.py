import time

from aw import SeaOfStarsAW
from cases.hongguo_common import HongguoCase


class PerformanceDynamic_hongguomianfeiduanju_0020(HongguoCase):
    """Excel 7.0.2：倍速、评论、搜索与横竖屏播放。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动红果免费短剧')
                self.start_hongguo()
            self.step(2, '长按首页推荐视频倍速播放')
            self.long_press_speed()
            self.step(3, '点击评论按钮')
            self.open_comments()
            self.step(4, '上滑3次，浏览评论')
            self.swipe_vertical(3, 0)
            self.step(5, '下滑3次，浏览评论')
            self.swipe_vertical(0, 3)
            self.step(6, '侧滑退出评论')
            self.close_comments_by_edge()
            self.step(7, '点击追剧')
            self.follow_current_drama()
            self.leave_player_to_feed()
            self.step(8, '点击剧场')
            self.open_theatre()
            self.step(9, '点击右上角搜索')
            self.device.click(180, 81)
            time.sleep(3)
            self.wait_for('搜索', max_y=130, timeout=8)
            self.step(10, '搜索仙帝')
            self.search('仙帝')
            self.step(11, '上滑3次，浏览搜索结果')
            self.swipe_vertical(3, 0)
            self.step(12, '下滑3次，浏览搜索结果')
            self.swipe_vertical(0, 3)
            self.step(13, '点击进入第一条搜索结果')
            self.open_first_search_result()
            self.step(14, '竖屏观看视频10s')
            time.sleep(10)
            self.step(15, '切换至横屏观看视频20s')
            self.enter_fullscreen()
            time.sleep(20)
            self.step(16, '返回剧场界面')
            self.return_search_video_to_theatre()
            self.step(17, '点击首页')
            self.tap('首页', min_y=760, wait=3)
            with self.capture_trace(iteration, 18):
                self.step(18, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
