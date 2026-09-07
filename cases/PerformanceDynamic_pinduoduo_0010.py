import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_pinduoduo_0010(Case):
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

            logging.info('启动拼多多')
            # SeaOfStarsAW.trace_thread.add_log('拼多多', '拼多多')
            SeaOfStarsAW.ut_device.click(0.613, 0.692)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('拼多多', '拼多多首页浏览')
            logging.info('上滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击搜索栏')
            # SeaOfStarsAW.trace_thread.add_log('拼多多', '搜索页面浏览')
            SeaOfStarsAW.ut_device.click(0.53, 0.075)
            time.sleep(3)
            logging.info('输入华为手机')
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('上滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('拼多多', '商品详情浏览')
            logging.info('点击第一个商品')
            SeaOfStarsAW.ut_device.click(0.17, 0.645)
            time.sleep(2)
            logging.info('上滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('拼多多', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')