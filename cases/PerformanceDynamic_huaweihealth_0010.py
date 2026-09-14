from aw import SeaOfStarsAW
from cases.huaweihealth_common import HuaweiHealthCase


class PerformanceDynamic_huaweihealth_0010(HuaweiHealthCase):
    """Excel 7.0.2：户外跑步、健康今日页和三叶草详情。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动华为运动健康')
                self.start_app(wait=5)
            self.normalize_home_after_launch()
            self.step(2, '点击切换至锻炼页面，然后点击GO进入运动计时界面')
            self.open_outdoor_running()
            self.step(3, '15s后长按结束运动')
            self.finish_short_workout(seconds=15)
            self.step(4, '点击屏幕底部今日')
            self.open_today()
            self.step(5, '点击三叶草查看详情')
            self.open_clover_details()
            self.step(6, '上滑1次，下滑1次，浏览详情页面')
            self.browse(up=1, down=1)
            self.step(7, '返回华为运动健康主界面')
            self.return_health_main()
            with self.capture_trace_5s(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
