import logging
import time
from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase


class PerformanceDynamic_xianyu_0020(WdaCase):
    APP_NAME = '闲鱼'
    STEP_INTERVAL = 0
    all_app_package_list = ['']
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False
    #     清空后台

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        logging.info("用例开始执行")
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(2)

        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '打开闲鱼，等待10s')
                SeaOfStarsAW.ut_device.swipe_left()
                SeaOfStarsAW.ut_device.click(0.37, 0.713)
                time.sleep(10)

            self.step(2, '切换到新发，上滑3次，下滑3次，每次停留2s')
            SeaOfStarsAW.ut_device.click(0.288, 0.134)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            self.step(3, '切换到服饰，上滑3次，下滑3次，每次停留2s')
            SeaOfStarsAW.ut_device.click(0.713, 0.13)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            with self.capture_trace(iteration, 4):
                self.step(4, '返回闲鱼首页，返回Home页面，停留2s')
                SeaOfStarsAW.ut_device.click(0.054, 0.089)
                SeaOfStarsAW.ut_device.home()
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_right()

        logging.info('用例执行结束')
