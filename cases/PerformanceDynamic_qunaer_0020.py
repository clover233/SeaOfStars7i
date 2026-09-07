import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qunaer_0020(Case):
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

            logging.info('启动去哪旅行')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '去哪旅行')
            SeaOfStarsAW.ut_device.click(0.156, 0.703)
            time.sleep(2)
            logging.info('点击机票')   # 无法刷新机票
            SeaOfStarsAW.ut_device.click(0.12, 0.314)
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device.click(0.506, 0.579)
            time.sleep(2)

            logging.info('点击火车高铁')
            SeaOfStarsAW.ut_device.click(0.44, 0.311)
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device.click(0.51, 0.508)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.056, 0.073)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.05, 0.075)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('去哪儿旅行', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')