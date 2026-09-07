import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_meituan_0080(Case):
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
            step = 0
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动美团（停留3s）
            logging.info('启动美团，等待3s')
            SeaOfStarsAW.trace_thread.add_log('美团', '进入外卖美食')
            SeaOfStarsAW.ut_device.session().app_activate('com.meituan.imeituan')
            time.sleep(3)

            # 2.点击美食团购（停留1s）
            logging.info('2、点击美食团购')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击美食团购')
            SeaOfStarsAW.ut_device.click(0.309, 0.191, 0.50)
            time.sleep(1)

            # 3.上滑5次浏览美食团购页面（停留1s）
            logging.info('3、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 4.下滑5次浏览美食团购页面（停留1s）
            logging.info('4、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('美团', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 5.点击美食餐厅下方第一个商家（停留1s）
            logging.info('5.点击美食餐厅下方第一个商家')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击美食餐厅下方第一个商家')
            SeaOfStarsAW.ut_device.click(0.578, 0.559, 0.30)
            time.sleep(1)

            # 6.上滑3次浏览商家页面（停留1s）
            logging.info('6.上滑3次浏览商家页面')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑3次浏览商家页面')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 7.下滑3次浏览商家页面（停留1s）
            logging.info('7.下滑3次浏览商家页面')
            SeaOfStarsAW.trace_thread.add_log('美团', '下滑3次浏览商家页面')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 10.点击第一个团购商品（停留1s）
            logging.info('10.点击第一个团购商品')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击第一个团购商品')
            SeaOfStarsAW.ut_device.click(0.484, 0.686, 0.30)
            time.sleep(1)

            # 11.返回首页（停留1s）
            logging.info('11.返回首页')
            SeaOfStarsAW.trace_thread.add_log('美团', '返回首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 12.上滑返回桌面（停留1s）
            logging.info('12.上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑返回桌面')
            SeaOfStarsAW.swipe_to_launcher()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.meituan.imeituan')

        logging.info('用例执行结束')