import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hwvmall_0020(Case):
    all_app_package_list = ['com.vmall.ios']
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
        SeaOfStarsAW.trace_thread.add_log('华为商城', description)

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

    def _browse(self, count):
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """华为商城浏览分类、商品详情、评价和客服页面。"""
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
                self._log_step('1、启动华为商城')
                device.app_activate('com.vmall.ios')
                time.sleep(8)

                self._log_step('2、点击分类')
                self._click('分类', 0.3, 0.95)

                self._log_step('3、上滑5次、下滑5次浏览分类')
                self._browse(5)

                self._log_step('4、查看商品详情，返回分类后再次进入商品详情页')
                device.click(0.65, 0.30)
                time.sleep(2)
                self._swipe_back()
                device.click(0.65, 0.30)
                time.sleep(2)

                self._log_step('5、查看商品详情')
                time.sleep(2)

                self._log_step('6、上滑5次、下滑5次浏览商品详情')
                self._browse(5)

                self._log_step('7、商品详情上滑1次')
                device.swipe_up()
                time.sleep(1)

                self._log_step('8、点击评价')
                self._click('评价', 0.5, 0.88, contains=True)

                self._log_step('9、点击查看全部宝贝评价')
                self._click('查看全部', 0.85, 0.20, contains=True)

                self._log_step('10、上滑5次、下滑5次浏览评价')
                self._browse(5)

                self._log_step('11、返回商品详情')
                self._swipe_back()

                self._log_step('12、点击客服')
                self._click('客服', 0.15, 0.92, contains=True)

                self._log_step('13、返回商品详情')
                self._swipe_back()

                self._log_step('14、返回华为商城主界面')
                for _ in range(3):
                    home_tab = device(label='首页', timeout=1)
                    if home_tab.exists:
                        home_tab.click()
                        time.sleep(2)
                        break
                    self._swipe_back()
                else:
                    raise RuntimeError('未能返回华为商城主界面，请校准页面返回层级')

                self._log_step('15、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
