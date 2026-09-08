import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hwvmall_0010(Case):
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

    def _open_next_banner(self, x, y):
        self._swipe_back()
        SeaOfStarsAW.ut_device.swipe(0.8, 0.25, 0.2, 0.25, duration=0.5)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """华为商城浏览轮播图、搜索结果和商品详情。"""
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
                time.sleep(6)

                self._log_step('2、点击第一个轮播图，进入轮播图详情页')
                device.click(0.5, 0.25)
                time.sleep(2)

                self._log_step('3、浏览第一个轮播图详情页，上滑3次、下滑3次')
                self._browse(3)

                self._log_step('4、点击第二个轮播图，进入轮播图详情页')
                self._open_next_banner(0.5, 0.25)

                self._log_step('5、浏览第二个轮播图详情页，上滑3次、下滑3次')
                self._browse(3)

                self._log_step('6、点击第三个轮播图，进入轮播图详情页')
                self._open_next_banner(0.5, 0.25)

                self._log_step('7、浏览第三个轮播图详情页，上滑3次、下滑3次')
                self._browse(3)

                self._log_step('8、点击搜索框，搜索p60')
                self._swipe_back()
                self._click('搜索', 0.5, 0.08, contains=True)
                device().set_text('p60')
                time.sleep(1)
                self._click('搜索', 0.9, 0.08)

                self._log_step('9、浏览搜索结果，上滑5次、下滑5次')
                self._browse(5)

                self._log_step('10、点击第一件商品，进入商品详情页')
                device.click(0.3, 0.35)
                time.sleep(2)

                # Excel 原表连续使用了两个“10”，保留原步骤编号。
                self._log_step('10、浏览商品详情，上滑6次、下滑6次')
                self._browse(6)

                self._log_step('12、返回华为商城主界面')
                for _ in range(3):
                    home_tab = device(label='首页', timeout=1)
                    if home_tab.exists:
                        home_tab.click()
                        time.sleep(2)
                        break
                    self._swipe_back()
                else:
                    raise RuntimeError('未能返回华为商城主界面，请校准页面返回层级')

                self._log_step('13、华为商城首页上滑6次、下滑6次')
                self._browse(6)

                self._log_step('14、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
