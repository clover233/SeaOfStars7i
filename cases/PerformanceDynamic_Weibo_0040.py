import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Weibo_0040(Case):
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
        # if SeaOfStarsAW.ut_device.locked():
        #     SeaOfStarsAW.ut_device.unlock()
        #     time.sleep(2)

        for test_time in range(0, self.TEST_TIME):
            step = 0
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动微博
            logging.info('启动微博')
            SeaOfStarsAW.trace_thread.add_log('微博', '打开微博,等待3s')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.6)
            time.sleep(10)

            # 2、点击发现，等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '点击发现，等待1s')
            SeaOfStarsAW.ut_device.click(0.507, 0.942)
            time.sleep(1)

            # 3、点击搜索栏
            SeaOfStarsAW.trace_thread.add_log('微博', '点击搜索栏')
            SeaOfStarsAW.ut_device.click(0.391, 0.087)
            time.sleep(2)
            # 4、输入 动态测试 等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '输入 动态测试 等待1s')
            SeaOfStarsAW.ut_device().set_text("动态测试")
            time.sleep(1)

            # 5、点击搜索 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '点击搜索')
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 6、点击用户 等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '点击用户，等待1s')
            SeaOfStarsAW.ut_device(labelContains="用户").click()
            time.sleep(1)

            # 7、点击动态测试用户 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '点击评论，等待2s')
            SeaOfStarsAW.ut_device.click(0.459, 0.294)
            time.sleep(2)

            # 8、点击第一条微博 浏览 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '点击第一条微博 浏览 等待2s')
            SeaOfStarsAW.ut_device(labelContains="正文").click()
            time.sleep(2)

            # 9、上滑返回到home 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '上滑返回到home 等待2s')
            for i in range(4):
                SeaOfStarsAW.ut_device.click(0.044, 0.086)
            SeaOfStarsAW.ut_device(labelContains="微博").click()
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

        logging.info('用例执行结束')