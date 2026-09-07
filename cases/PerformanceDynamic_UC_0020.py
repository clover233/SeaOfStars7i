import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_UC_0020(Case):
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

            logging.info('启动UC浏览器')
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '启动UC浏览器')
            SeaOfStarsAW.ut_device.click(0.156, 0.354)
            # logging.info('等待2s')
            # time.sleep(2)
            # SeaOfStarsAW.ut_device.swipe_up()
            # time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '搜索栏新闻浏览')
            logging.info('点击搜索栏')
            SeaOfStarsAW.ut_device.click(0.393, 0.138)
            time.sleep(2)
            logging.info('输入大话天仙')
            SeaOfStarsAW.ut_device.send_keys('大话天仙')
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '搜索发现浏览')
            logging.info('点击第一条搜索发现')
            SeaOfStarsAW.ut_device.click(0.193, 0.172)
            time.sleep(2)
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.856, 0.938)
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')