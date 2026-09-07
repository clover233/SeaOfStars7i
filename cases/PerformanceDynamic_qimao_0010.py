import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qimao_0010(Case):
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

        for test_time in range(0, self.TEST_TIME):
            # step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            logging.info('启动爱奇艺')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '启动七猫')
            SeaOfStarsAW.ut_device.click(0.163, 0.125)
            time.sleep(8)
            logging.info('点击书架')
            SeaOfStarsAW.ut_device(label='书架').click()
            time.sleep(2)
            for _ in range(3):
                logging.info('点击书籍进行阅读')
                SeaOfStarsAW.ut_device.click(0.156, 0.228)
                time.sleep(2)
                logging.info('左滑5次，右滑5次')
                for _ in range(5):
                    SeaOfStarsAW.ut_device.swipe_left()
                    time.sleep(1)
                for _ in range(5):
                    SeaOfStarsAW.ut_device.swipe_right()
                    time.sleep(1)
                logging.info('返回')
                SeaOfStarsAW.ut_device(label='返回').click()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击书城')
            SeaOfStarsAW.ut_device(label='书城').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')