import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weipinhui_0030(Case):
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
            app_name ="唯品会"

            step1 = "'1、打开唯品会,等待10s'"
            logging.info('启动唯品会')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.367, 0.593)
            time.sleep(10)

            step2 = "2、向上抛滑3次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()

            step3 = "3、点击tab栏运动 等待3s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device(label="运动").click()
            time.sleep(3)

            step4 = "4、向上抛滑3次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()

            step5 = "5、点击 唯品奥莱"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.click(0.121, 0.423)

            step6 = "6、浏览详情 上滑2次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step7 = "7、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device.swipe(0.025,0.5, 0.925,0.5)
            time.sleep(2)

            step8 = "8、返回首页 返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')