import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Dingding_0010(Case):
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
            app_name ="钉钉"

            step1 = "'1、打开钉钉,等待10s'"
            logging.info('启动钉钉')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.click(0.384, 0.367)
            time.sleep(10)

            step2 = "2、点击 左下角 消息图标"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(labelContains="消息").click()
            time.sleep(1)

            step3 = "3、点击 欢迎试用钉钉群"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device(labelContains="新手体验群").click()
            time.sleep(1)

            step4 = "4、上滑2次 下滑2次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step5 = "5、点进 消息输入框 2s 输入 你好 停留2s 点击发送"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.click(0.432, 0.907)
            time.sleep(2)
            SeaOfStarsAW.ut_device().set_text("你好")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.874, 0.875)

            step6 = "6、点击右上角 的更多"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.924, 0.09)
            time.sleep(1)

            step7 = "7、上下滑动各一次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step8 = "8、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.058, 0.087)
            SeaOfStarsAW.ut_device.click(0.058, 0.087)
            SeaOfStarsAW.ut_device(label="工作台").click()

            step9 = "9、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)


        logging.info('用例执行结束')