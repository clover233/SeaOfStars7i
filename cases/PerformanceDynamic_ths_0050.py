import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_ths_0050(Case):
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

            logging.info('启动同花顺')
            # SeaOfStarsAW.trace_thread.add_log('同花顺', '启动同花顺')
            SeaOfStarsAW.ut_device.click(0.156, 0.353)
            logging.info('等待5s')
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('同花顺', '自选格力电器股票')
            logging.info('点击自选')
            SeaOfStarsAW.ut_device(label='自选').click()
            time.sleep(2)
            logging.info('点击搜索栏')
            SeaOfStarsAW.ut_device.click(0.926, 0.075)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('格力电器')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('点击格里电器股票')
            SeaOfStarsAW.ut_device.click(0.126, 0.231)
            time.sleep(2)
            logging.info('加自选')
            SeaOfStarsAW.ut_device.click(0.69, 0.935)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('同花顺', '格力股票浏览，上滑3次，下滑3次')
            logging.info('上滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('点击删自选')
            SeaOfStarsAW.ut_device.click(0.69, 0.932)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('同花顺', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')