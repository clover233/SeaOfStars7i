from aw import SeaOfStarsAW
from cases.weather_common import WeatherCase


class PerformanceDynamic_weather_0010(WeatherCase):
    """天气主页和城市切换（以用户补充的8步为准）。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动天气')
                self.start_weather()
            self.step(2, '主页浏览，上下各滑动5次')
            self.browse(5, 5)
            self.step(3, '点击天气主页面右下方三点三线')
            self.open_city_list()
            self.step(4, '点击左上按钮，再返回（单击空白）')
            self.open_and_dismiss_city_menu()
            self.step(5, '点击城市管理界面的第一个城市')
            self.open_first_managed_city()
            self.step(6, '滑动切换不同城市，左滑5次，右滑5次，重复操作5次')
            self.switch_cities(left=5, right=5, repeats=5)
            self.step(7, '返回天气主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
