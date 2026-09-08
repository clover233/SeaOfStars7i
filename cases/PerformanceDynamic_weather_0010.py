import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weather_0010(Case):
    # tidevice applist 可能不返回系统应用，因此不在 set_up 中校验包名。
    all_app_package_list = []
    TEST_TIME = 1
    APP_PACKAGE = 'com.apple.weather'

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('天气', description)

    def _click(self, label, x, y, contains=True):
        selector_args = {
            'labelContains' if contains else 'label': label,
            'timeout': 2,
        }
        element = SeaOfStarsAW.ut_device(**selector_args)
        if element.exists:
            element.click()
        else:
            logging.warning('未找到控件“%s”，使用待校准坐标：%s', label, (x, y))
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """天气主页、城市管理和多日天气浏览。"""
        logging.info('用例开始执行')
        device = SeaOfStarsAW.ut_device
        if device.locked():
            device.unlock()
            time.sleep(2)

        for test_time in range(self.TEST_TIME):
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'step_' + str(test_time),
                self.screenshot_dir_path,
            )
            try:
                self._log_step('1、启动天气')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('2、主页浏览，上滑5次、下滑5次')
                for _ in range(5):
                    device.swipe_up()
                    time.sleep(1)
                for _ in range(5):
                    device.swipe_down()
                    time.sleep(1)

                self._log_step('3、点击天气主页面右上方四个角')
                device.click(0.92, 0.08)
                time.sleep(2)

                self._log_step('4、点击管理城市')
                self._click('管理城市', 0.5, 0.15)

                self._log_step('5、点击城市管理界面的第一个城市')
                device.click(0.5, 0.22)
                time.sleep(2)

                self._log_step('6、左滑5次、右滑5次切换城市，重复5次')
                for _ in range(5):
                    for _ in range(5):
                        device.swipe_left()
                        time.sleep(1)
                    for _ in range(5):
                        device.swipe_right()
                        time.sleep(1)

                self._log_step('7、点击查看更多天气')
                self._click('查看更多天气', 0.5, 0.82)

                self._log_step('8、左右各滑动1次查看近日天气')
                device.swipe_left()
                time.sleep(1)
                device.swipe_right()
                time.sleep(2)

                self._log_step('9、返回天气主界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('10、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
