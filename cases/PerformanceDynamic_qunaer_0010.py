import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qunaer_0010(Case):
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
            logging.info('点击机票')
            SeaOfStarsAW.ut_device.click(0.12, 0.314)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '浏览机票搜索结果')
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device.click(0.506, 0.579)
            time.sleep(2)
            logging.info('点击明天')
            SeaOfStarsAW.ut_device.click(0.273, 0.129)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('去哪儿旅行', '浏览搜索结果')
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑6次')
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击第一个方案')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '浏览第一个方案')
            SeaOfStarsAW.ut_device.click(0.17, 0.233)
            time.sleep(3)
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.05, 0.075)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.05, 0.075)
            time.sleep(2)
            logging.info('点击酒店')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '查看酒店')
            SeaOfStarsAW.ut_device.click(0.16, 0.242)
            time.sleep(2)
            logging.info('点击城市')
            SeaOfStarsAW.ut_device.click(0.126, 0.248)
            time.sleep(2)
            logging.info('点击西安')
            SeaOfStarsAW.ut_device(label='西安').click()
            time.sleep(2)
            logging.info('点击酒店订单')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '查看酒店订单')
            SeaOfStarsAW.ut_device.click(0.853, 0.579)
            time.sleep(2)
            logging.info('返回上一页')
            SeaOfStarsAW.ut_device.click(0.073, 0.07)
            time.sleep(2)
            logging.info('点击开始搜索')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '浏览搜索页')
            SeaOfStarsAW.ut_device.click(0.473, 0.248)
            time.sleep(2)
            logging.info('上滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击搜索的第一条')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '查看搜索结果')
            SeaOfStarsAW.ut_device.click(0.14, 0.219)
            time.sleep(2)
            logging.info('点击酒店图片')
            # SeaOfStarsAW.trace_thread.add_log('去哪旅行', '浏览酒店图片')
            SeaOfStarsAW.ut_device.click(0.16, 0.311)
            time.sleep(2)
            logging.info('左滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            logging.info('右滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.046, 0.075)
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.923, 0.075)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('去哪儿旅行', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')