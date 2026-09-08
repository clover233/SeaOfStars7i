import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_mms_0010(Case):
    # tidevice applist 可能不返回系统应用，因此不在 set_up 中校验包名。
    all_app_package_list = []
    TEST_TIME = 1
    APP_PACKAGE = 'com.apple.MobileSMS'

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('信息', description)

    def _swipe_back(self):
        SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
        time.sleep(2)

    def _browse(self, count):
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """信息应用浏览通知信息和两条通知详情。"""
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
                self._log_step('1、启动信息')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('2、点击通知信息，进入通知信息页面')
                notifications = device(labelContains='通知信息', timeout=2)
                if notifications.exists:
                    notifications.click()
                else:
                    logging.warning('未找到“通知信息”，使用待校准坐标：%s',
                                    (0.5, 0.22))
                    device.click(0.5, 0.22)
                time.sleep(2)

                self._log_step('3、浏览通知信息，上滑5次、下滑5次')
                self._browse(5)

                self._log_step('4、打开一条通知信息进行查看，重复操作2次')
                for _ in range(2):
                    device.click(0.5, 0.20)
                    time.sleep(2)
                    self._swipe_back()

                self._log_step('5、返回信息主界面')
                self._swipe_back()

                self._log_step('6、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
