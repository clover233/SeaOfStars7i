import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xianyu_0020(Case):
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

            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            app_name ="闲鱼"

            step1 = "打开闲鱼,等待10s"
            logging.info('启动闲鱼')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.37, 0.713)
            time.sleep(10)

            step2 = "切换到新发 上滑3次 下滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device.click(0.288, 0.134)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            step3 = "切换到服饰 上滑3次 下滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device.click(0.713, 0.13)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            step4 = "返回闲鱼首页 返回home页面 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device.click(0.054, 0.089)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_right()

        logging.info('用例执行结束')