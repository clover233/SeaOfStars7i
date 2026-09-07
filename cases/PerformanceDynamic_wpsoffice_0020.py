import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_wpsoffice_0020(Case):
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
            app_name ="wpsoffice"

            step1 = "'1、打开wps,等待10s'"
            logging.info('启动wps')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.856, 0.591)
            time.sleep(10)

            step2 = "2、点击底部找模版 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="找模版").click()

            step3 = "3、滑动浏览上滑2次 下滑2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step4 = "4、点击首页 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)

            step5 = "5、点击右下角红色 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.click(0.892, 0.765)
            time.sleep(1)


            step6 = "6、点击文字 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.164,0.567)
            time.sleep(1)

            step7 = "7、点击空白文档 输入动态性能测试 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="空白文档").click()
            time.sleep(5)
            SeaOfStarsAW.ut_device().set_text("动态性能测试")

            step12 = "8、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.936,0.086)
            SeaOfStarsAW.ut_device.click(0.504,0.864)
            SeaOfStarsAW.ut_device.click(0.062,0.077)
            time.sleep(1)

            step13 = "9、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')