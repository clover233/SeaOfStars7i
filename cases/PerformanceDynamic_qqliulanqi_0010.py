import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qqliulanqi_0010(Case):
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

            logging.info('启动QQ浏览器')
            # SeaOfStarsAW.trace_thread.add_log('QQ浏览器', '启动QQ浏览器')
            SeaOfStarsAW.ut_device.click(0.613, 0.701)
            time.sleep(8)
            # SeaOfStarsAW.trace_thread.add_log('QQ浏览器', '浏览放映厅')
            logging.info('点击搜索框')
            SeaOfStarsAW.ut_device.click(0.281, 0.144)
            time.sleep(2)
            logging.info('输入优酷')
            SeaOfStarsAW.ut_device.send_keys('优酷')
            time.sleep(1)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击第一个搜索结果，进入优酷官网')
            # SeaOfStarsAW.trace_thread.add_log('QQ浏览器', '浏览优酷官网')
            SeaOfStarsAW.ut_device.click(0.268, 0.241)
            # SeaOfStarsAW.ut_device(label='- 中国领先视频网站').click()
            time.sleep(1)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击电视剧')
            # SeaOfStarsAW.trace_thread.add_log('QQ浏览器', '启动浏览优酷官网电视剧界面')
            SeaOfStarsAW.ut_device(label='电视剧').click()
            time.sleep(1)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回')
            # SeaOfStarsAW.trace_thread.add_log('QQ浏览器', '返回桌面')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='后退').click()
            time.sleep(2)
            logging.info('返回首页')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='后退').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')