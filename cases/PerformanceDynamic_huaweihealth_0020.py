from aw import SeaOfStarsAW
from cases.huaweihealth_common import HuaweiHealthCase


class PerformanceDynamic_huaweihealth_0020(HuaweiHealthCase):
    """Excel 7.0.2：设备页重复进入扫一扫。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动运动健康')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击设备，进入设备界面')
            self.open_devices()
            self.step(3, '点击右上角更多图标，进入更多功能页面')
            self.open_more_functions()
            self.step(4, '点击扫一扫，进入扫一扫页面后返回，重复3次')
            for index in range(3):
                self.scan_and_return()
                if index < 2:
                    self.open_more_functions()
            self.step(5, '返回运动健康主界面')
            self.return_health_main()
            with self.capture_trace_5s(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
