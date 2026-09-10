from aw import SeaOfStarsAW
from cases.baidu_common import BaiduMapCase


class PerformanceDynamic_baidumap_0010(BaiduMapCase):
    """Excel 7.0.2：百度地图导航至西安钟楼。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动百度地图')
                self.start_baidu_map()
            self.step(2, '搜索框搜索钟楼')
            self.search_clock_tower()
            self.step(3, '选择西安钟楼')
            self.select_xian_clock_tower()
            self.step(4, '点击到这去')
            self.go_to_destination()
            self.step(5, '点击开始导航')
            self.start_navigation()
            self.step(6, '点击退出导航')
            self.exit_navigation()
            self.step(7, '返回百度地图主界面')
            self.return_map_home()
            with self.capture_trace(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
