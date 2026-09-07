import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Weibo_0020(Case):
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

            # 1、启动微博
            logging.info('启动微博')
            SeaOfStarsAW.trace_thread.add_log('微博', '1、打开微博,等待3s')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.6)
            time.sleep(10)

            # 2、主页面 等待3s
            SeaOfStarsAW.trace_thread.add_log('微博', '2、主页面 等待3s')
            time.sleep(3)

            # 3、点击推荐 等1s
            SeaOfStarsAW.trace_thread.add_log('微博', '3、点击推荐 等1s')
            SeaOfStarsAW.ut_device(labelContains="推荐").click()
            time.sleep(1)

            # 4、上滑5次，下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '4、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、点击关注 等1s
            SeaOfStarsAW.trace_thread.add_log('微博', '5、点击关注 等1s')
            SeaOfStarsAW.ut_device(labelContains="关注").click()
            time.sleep(1)

            # 6、上滑5次、下滑6次，每次等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '6、上滑5次、下滑6次，每次等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 7、上滑返回到home 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '7、上滑返回到home 等待2s')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

        logging.info('用例执行结束')