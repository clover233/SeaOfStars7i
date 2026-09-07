import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_tielu12306_0010(Case):
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

            logging.info('启动铁路12306')
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '启动12306')
            SeaOfStarsAW.ut_device.click(0.843, 0.697)
            logging.info('等待5s')
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '首页抛滑，上滑1次，下滑2次')
            logging.info('上滑1次')   # 抛滑暂用swipe代替
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            logging.info('下滑2次')
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击查询车票')
            SeaOfStarsAW.ut_device(label='查询车票').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '火车票浏览，上滑2次，下滑3次')
            logging.info('上滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '火车票浏览tab切换')
            logging.info('点击耗时最短')
            # SeaOfStarsAW.ut_device(label='耗时最短').click()
            SeaOfStarsAW.ut_device.click(0.303, 0.947)
            time.sleep(1)
            logging.info('点击最早发车')
            # SeaOfStarsAW.ut_device(label='最早发车').click()
            SeaOfStarsAW.ut_device.click(0.5, 0.947)
            time.sleep(1)
            logging.info('点击价格最低')
            # SeaOfStarsAW.ut_device(label='价格最低').click()
            SeaOfStarsAW.ut_device.click(0.693, 0.949)
            time.sleep(1)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(1)
            logging.info('返回桌面')
            # SeaOfStarsAW.trace_thread.add_log('12306', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')