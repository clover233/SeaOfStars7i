import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_tencentnews_0010(Case):
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

            logging.info('启动腾讯新闻')
            # SeaOfStarsAW.trace_thread.add_log('腾讯新闻', '启动腾讯新闻')
            SeaOfStarsAW.ut_device.click(0.62, 0.695)
            logging.info('等待5s')
            time.sleep(8)
            # SeaOfStarsAW.trace_thread.add_log('腾讯新闻', '主页浏览，上滑5次，下滑2次')
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('左滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            logging.info('右滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯新闻', '浏览视新闻界面)
            logging.info('新闻')
            SeaOfStarsAW.ut_device(label='新闻').click()
            time.sleep(2)
            logging.info('浏览为你推荐，上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯新闻', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')