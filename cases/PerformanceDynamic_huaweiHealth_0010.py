import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_huaweiHealth_0010(Case):
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
        """华为运动健康浏览锻炼页面。"""
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
                self._log_step('1、启动华为运动健康')
                device.app_activate('com.huawei.iossporthealth')
                time.sleep(3)

                self._log_step('2、点击锻炼，然后点击GO进入运动计时界面')
                self._click('锻炼', 0.5, 0.95)
                self._click('GO', 0.5, 0.72)

                self._log_step('3、15s后长按结束运动')
                time.sleep(15)
                end_button = device(labelContains='结束', timeout=2)
                if end_button.exists:
                    center = end_button.bounds.center
                    device.tap_hold(center.x, center.y, duration=2)
                else:
                    logging.warning('未找到结束按钮，使用待校准坐标：%s',
                                    (0.5, 0.82))
                    device.tap_hold(0.5, 0.82, duration=2)
                time.sleep(3)

                self._log_step('4、点击屏幕底部今日')
                self._click('今日', 0.2, 0.92)

                self._log_step('5、点击三叶草查看详情')
                self._click('三叶草', 0.5, 0.45, contains=True)

                self._log_step('6、上滑1次、下滑1次，浏览详情页面')
                device.swipe_up()
                time.sleep(1)
                device.swipe_down()
                time.sleep(1)

                self._log_step('7、返回华为运动健康主界面')
                self._swipe_back()
                health_tab = device(label='健康', timeout=2)
                if health_tab.exists:
                    health_tab.click()
                    time.sleep(2)

                self._log_step('8、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
