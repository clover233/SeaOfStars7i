import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_UC_0010(Case):
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
            SeaOfStarsAW.ut_device.click(0.16, 0.354)
            logging.info('等待2s')
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '首页切换浏览')
            logging.info('左滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('右滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '发现页面浏览)
            logging.info('点击发现')
            SeaOfStarsAW.ut_device(label='发现').click()
            time.sleep(1)
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑6次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击推荐')
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '推荐页面新闻浏览')
            SeaOfStarsAW.ut_device(label='推荐').click()
            time.sleep(2)
            logging.info('点击第一条新闻')
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '点击推荐下面第一条新闻滑动浏览')
            SeaOfStarsAW.ut_device.click(0.42, 0.199)
            time.sleep(2)
            logging.info('上滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='首页').click()
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '首页浏览')
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('UC浏览器', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')