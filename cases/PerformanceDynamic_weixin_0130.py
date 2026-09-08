import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0130(Case):
    all_app_package_list = ['com.tencent.xin']
    TEST_TIME = 1
    APP_PACKAGE = 'com.tencent.xin'

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
        SeaOfStarsAW.trace_thread.add_log('微信', description)

    def _click(self, label, x, y, contains=False, wait=2):
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
        time.sleep(wait)

    def _click_any(self, labels, x, y, contains=False, wait=2):
        for label in labels:
            selector_args = {
                'labelContains' if contains else 'label': label,
                'timeout': 1,
            }
            element = SeaOfStarsAW.ut_device(**selector_args)
            if element.exists:
                element.click()
                time.sleep(wait)
                return
        logging.warning('未找到控件%s，使用待校准坐标：%s', labels, (x, y))
        SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(wait)

    def _browse(self, up_count, down_count=None):
        down_count = up_count if down_count is None else down_count
        for _ in range(up_count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(down_count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    def _start_trace(self, test_time):
        SeaOfStarsAW.start_trace(
            self.trace_dir_path,
            self.__class__.__name__,
            'step_' + str(test_time),
            self.screenshot_dir_path,
        )

    def _launch_weixin(self):
        SeaOfStarsAW.ut_device.app_activate(self.APP_PACKAGE)
        time.sleep(5)

    def _return_home(self):
        SeaOfStarsAW.swipe_to_launcher()
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """微信新闻类公众号浏览。"""
        logging.info('用例开始执行')
        device = SeaOfStarsAW.ut_device
        if device.locked():
            device.unlock()
            time.sleep(2)

        for test_time in range(self.TEST_TIME):
            self._start_trace(test_time)
            try:
                self._log_step('1、启动微信')
                self._launch_weixin()

                self._log_step('2、点击通讯录')
                self._click('通讯录', 0.37, 0.95)

                self._log_step('3、点击公众号')
                self._click('公众号', 0.5, 0.40)

                self._log_step('4、点击腾讯新闻公众号名片')
                self._click('腾讯新闻', 0.5, 0.25, contains=True)

                self._log_step('5、点击底部早报晚报，然后点击晚报')
                device.click(0.30, 0.95)
                time.sleep(1)
                self._click('晚报', 0.30, 0.80, contains=True)

                self._log_step('6、浏览晚报，上滑5次、下滑5次')
                self._browse(5)

                self._log_step('7、返回公众号列表界面')
                for _ in range(2):
                    device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                    time.sleep(2)

                self._log_step('8、点击央视新闻公众号名片')
                self._click('央视新闻', 0.5, 0.35, contains=True)

                self._log_step('9、点击底部文博日历查看详情')
                device.click(0.30, 0.95)
                time.sleep(1)
                self._click('文博日历', 0.30, 0.80, contains=True)

                self._log_step('10、浏览文博日历，上滑2次、下滑2次')
                self._browse(2)

                self._log_step('11、返回央视新闻对话界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('12、点击底部夜读查看详情')
                device.click(0.70, 0.95)
                time.sleep(1)
                self._click('夜读', 0.70, 0.80, contains=True)

                self._log_step('13、浏览夜读，上滑2次、下滑2次')
                self._browse(2)

                self._log_step('14、返回微信首页')
                for _ in range(3):
                    device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                    time.sleep(2)
                self._click('微信', 0.12, 0.95)

                self._log_step('15、点击订阅号')
                self._click('订阅号', 0.5, 0.25, contains=True)

                self._log_step('16、点击腾讯新闻')
                self._click('腾讯新闻', 0.5, 0.25, contains=True)

                self._log_step('17、腾讯新闻页面下滑3次')
                for _ in range(3):
                    device.swipe_down()
                    time.sleep(1)

                self._log_step('18、返回微信主界面')
                for _ in range(2):
                    device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                    time.sleep(2)

                self._log_step('19、滑动返回Home页')
                self._return_home()
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
