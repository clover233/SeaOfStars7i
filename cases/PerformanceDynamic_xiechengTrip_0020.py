import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xiechengTrip_0020(Case):
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
            app_name ="携程"

            step1 = "'1、打开携程,等待10s'"
            logging.info('启动携程')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.626, 0.717)
            time.sleep(10)

            step2 = "2、点击机票 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="机票").click()

            step3 = "3、点击查询"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device(label="查询").click()


            step4 = "4、上滑3次 下滑4次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step5 = "5、查第一条结果"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.click(0.532, 0.226)

            step6 = "6、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)

            step7 = "7、点击火车票"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="火车票").click()

            step8 = "8、点击查询"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="查询").click()


            step9 = "9、上滑3次 下滑4次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            step10 = "10、查看第一条结果"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device.click(0.532, 0.226)

            step11 = "11、点击 预定 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.click(0.88, 0.349)

            step12 = "12、返回主界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)
            SeaOfStarsAW.ut_device.click(0.048, 0.084)

            step13 = "13、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')