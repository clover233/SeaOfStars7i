import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qq_0010(Case):
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

            logging.info('启动qq')
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '启动爱奇艺')
            SeaOfStarsAW.ut_device.click(0.62, 0.238)
            time.sleep(5)
            logging.info('点击动态')
            SeaOfStarsAW.ut_device.click(0.873, 0.929)
            time.sleep(2)
            logging.info('点击好友动态')
            SeaOfStarsAW.ut_device(label='好友动态').click()
            time.sleep(3)
            logging.info('点击我的头像进入空间')
            SeaOfStarsAW.ut_device.click(0.133, 0.236)
            time.sleep(2)
            logging.info('点击动态图片')
            SeaOfStarsAW.ut_device.click(0.05, 0.075)
            time.sleep(2)
            logging.info('左滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(3)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.123, 0.921)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')