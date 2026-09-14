from aw import SeaOfStarsAW
from cases.dianping_common import DianpingCase


class PerformanceDynamic_dazhongdianping_0020(DianpingCase):
    """浏览大众点评首页的美食、景点游玩和休闲玩乐分类。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动大众点评')
                self.start_dianping()
            self.step(2, '主页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击推荐旁边的美食')
            self.open_home_category('美食')
            self.step(4, '滑动浏览美食，上滑5次，下滑5次')
            self.browse(5, 5)
            self.return_from_category()
            self.step(5, '点击推荐旁边的景点游玩')
            self.open_home_category('景点游玩')
            self.step(6, '滑动浏览出行，上滑5次，下滑5次')
            self.browse(5, 5)
            self.return_from_category()
            self.step(7, '点击推荐旁边的休闲玩乐')
            self.open_home_category('休闲玩乐')
            self.step(8, '滑动浏览玩乐，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '返回大众点评主界面')
            self.return_from_category()
            with self.capture_trace(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
