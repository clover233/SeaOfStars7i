from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0070(DouyinCase):
    """Excel 7.0.2：浏览个人收藏、喜欢作品和我的钱包。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动抖音')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击我')
            self.open_me()
            self.step(3, '点击收藏')
            self.open_collection()
            self.step(4, '点第一个收藏的作品')
            self.open_first_own_video()
            self.step(5, '向上滑动3次，浏览收藏第一个作品页面')
            self.swipe_up_times(3)
            self.step(6, '返回我的页面')
            self.return_to_me()
            self.step(7, '点击喜欢')
            self.open_likes()
            self.step(8, '点第一个喜欢的作品')
            self.open_first_own_video()
            self.step(9, '向上滑动3次，浏览喜欢的作品页面')
            self.swipe_up_times(3)
            self.step(10, '返回我的页面')
            self.return_to_me()
            self.step(11, '点击我的钱包')
            self.open_wallet()
            self.step(12, '返回抖音主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 13):
                self.step(13, '滑动返回Home页')
                self.launcher()
