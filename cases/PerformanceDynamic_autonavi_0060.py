import time

from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0060(AutonaviCase):
    """Excel 7.0.2：导航期间切换小红书和抖音。"""

    all_app_package_list = [
        AutonaviCase.PACKAGE,
        AutonaviCase.XHS_PACKAGE,
        AutonaviCase.DOUYIN_PACKAGE,
    ]

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '点击搜索框')
            self.open_search()
            self.step(3, '输入西安北站并搜索')
            self.enter_search_text('西安北站')
            self.step(4, '点击第一个搜索结果的路线')
            self.tap_first_route()
            self.step(5, '点击开始导航')
            self.select_driving()
            self.start_navigation()
            self.step(6, '滑动返回Home页')
            self.launcher()
            self.step(7, '启动小红书')
            self.start_app(self.XHS_PACKAGE)
            self.step(8, '浏览首页，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '点击消息')
            self.tap('消息', min_y=760, fallback=(0.70, 0.94))
            self.step(10, '点击我')
            self.tap('我', min_y=760, fallback=(0.90, 0.94))
            self.step(11, '点击收藏')
            self.tap('收藏', fallback=(0.25, 0.49), wait=3)
            self.step(12, '浏览收藏页，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(13, '返回小红书主界面')
            self.tap('首页', min_y=760, fallback=(0.10, 0.94), wait=2)
            self.step(14, '滑动返回Home页')
            self.launcher()
            self.step(15, '启动高德地图')
            self.resume_navigation()
            self.step(16, '滑动返回Home页')
            self.launcher()
            self.step(17, '启动抖音')
            self.start_app(self.DOUYIN_PACKAGE)
            self.step(18, '首页观看10s')
            time.sleep(10)
            self.step(19, '浏览首页，上滑5次，下滑5次')
            self.browse(5, 5, wait=2)
            self.step(20, '点击顶部热点')
            self.tap('热点', max_y=180, fallback=(0.13, 0.10), wait=2)
            self.step(21, '浏览热点页面，上滑5次，下滑5次')
            self.browse(5, 5, wait=2)
            self.step(22, '点击推荐')
            self.tap('推荐', max_y=180, fallback=(0.81, 0.10), wait=2)
            self.step(23, '滑动返回Home页')
            self.launcher()
            self.step(24, '启动高德地图')
            self.resume_navigation()
            self.step(25, '退出导航')
            self.open_exit_navigation()
            self.confirm_exit_navigation()
            self.step(26, '返回高德地图主界面')
            self.return_autonavi_home()
            with self.capture_trace(iteration, 27):
                self.step(27, '滑动返回Home页')
                self.launcher()
