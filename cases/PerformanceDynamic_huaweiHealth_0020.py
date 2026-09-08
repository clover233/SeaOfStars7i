import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_huaweiHealth_0020(Case):
    all_app_package_list = ['com.huawei.iossporthealth']
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for package in self.all_app_package_list:
            if package not in phone_app_list:
                raise RuntimeError('未安装测试应用：{}'.format(package))
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('华为运动健康', description)

    def _click(self, label, x, y, contains=False):
        selector_args = {'labelContains' if contains else 'label': label, 'timeout': 2}
        element = SeaOfStarsAW.ut_device(**selector_args)
        if element.exists:
            element.click()
        else:
            logging.warning('未找到控件“%s”，使用待校准坐标：%s',
                            label, (x, y))
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(2)

    def _swipe_back(self):
        SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """华为运动健康浏览设备页面。"""
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
                self._log_step('1、启动运动健康')
                device.app_activate('com.huawei.iossporthealth')
                time.sleep(3)

                self._log_step('2、点击设备，进入设备界面')
                self._click('设备', 0.7, 0.95)

                self._log_step('3、点击右上角更多图标，进入更多功能页面')
                self._click('更多', 0.92, 0.08, contains=True)

                self._log_step('4、进入扫一扫页面后返回，重复3次')
                for _ in range(3):
                    self._click('扫一扫', 0.5, 0.25, contains=True)
                    for permission_label in ('允许', '好'):
                        permission = device(label=permission_label, timeout=1)
                        if permission.exists:
                            permission.click()
                            time.sleep(2)
                            break
                    self._swipe_back()

                self._log_step('5、返回运动健康主界面')
                self._swipe_back()
                health_tab = device(label='健康', timeout=2)
                if health_tab.exists:
                    health_tab.click()
                    time.sleep(2)

                self._log_step('6、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
