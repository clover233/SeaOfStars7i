from aw import SeaOfStarsAW
from cases.douyin_common import DouyinCase


class PerformanceDynamic_douyin_0060(DouyinCase):
    """Excel 7.0.2：浏览精选（长视频）、经验和热点频道。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动抖音')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击长视频')
            self.open_featured()
            self.step(3, '依次切换关注-团购-推荐，循环3次')
            for _ in range(3):
                self.open_follow_channel()
                self.open_group_buy()
                self.open_recommend()
            self.step(4, '点击长视频')
            self.open_featured()
            self.step(5, '上滑3次，下滑3次浏览长视频')
            self.browse(3, 3)
            self.step(6, '返回推荐页面')
            self.open_recommend()
            self.step(7, '点击顶部经验')
            self.open_experience()
            self.step(8, '上滑3次，下滑3次浏览经验')
            self.browse(3, 3)
            self.step(9, '点击热点')
            self.open_hotspot()
            self.step(10, '上滑3次，下滑3次浏览热点')
            self.browse(3, 3)
            self.step(11, '返回抖音主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 12):
                self.step(12, '滑动返回Home页')
                self.launcher()
