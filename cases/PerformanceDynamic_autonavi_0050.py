from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0050(AutonaviCase):
    """Excel 7.0.2：浏览地图并查看西安钟楼打车车型。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动高德地图')
                self.start_autonavi()
            self.step(2, '地图界面上滑1次浏览')
            self.browse(1, 0)
            self.step(3, '地图界面下滑1次浏览')
            self.browse(0, 1)
            self.step(4, '地图界面左滑1次浏览')
            self.device.swipe(0.75, 0.5, 0.25, 0.5, 0.3)
            self.step(5, '地图界面右滑1次浏览')
            self.device.swipe(0.25, 0.5, 0.75, 0.5, 0.3)
            self.step(6, '双指捏合放大，缩小当前位置地图')
            self.pinch_map()
            self.step(7, '点击下方打车tab页')
            self.open_taxi_tab()
            self.step(8, '点击目的地')
            self.tap('你要去哪儿', fallback=(0.25, 0.60), wait=2)
            self.step(9, '输入西安钟楼，搜索')
            self.enter_search_text('西安钟楼')
            self.step(10, '选择售票处')
            self.tap('售票处', wait=4)
            self.step(11, '选择下车点')
            self.tap('在这下车', wait=5)
            self.step(12, '上滑3次，下滑3次，浏览车型')
            self.browse(3, 3)
            self.step(13, '滑动返回打车tab页')
            self.device.swipe(0.01, 0.5, 0.85, 0.5, 0.3)
            self.step(14, '点击回到高德首页')
            self.return_autonavi_home()
            with self.capture_trace(iteration, 15):
                self.step(15, '滑动返回桌面')
                self.launcher()
