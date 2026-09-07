import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_zuoyebang_0020(Case):
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
            app_name ="作业帮"

            step1 = "'打开作业帮,等待10s'"
            logging.info('启动作业帮')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.847, 0.135)
            time.sleep(10)

            step2 = "点击搜索 输入成语故事 2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="aihome navi search").click()
            SeaOfStarsAW.ut_device().set_text("成语故事")
            time.sleep(2)


            step3 = "上滑3次 下滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # step4 = "点击查看更多 上滑一次 等待2s"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            # SeaOfStarsAW.ut_device.click(0.5, 0.913)
            # time.sleep(5)
            #
            # step5 = "点击 值得鼓励 2s"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            # SeaOfStarsAW.ut_device.click(0.077, 0.82)
            # SeaOfStarsAW.ut_device(label="camera close new").click()
            # time.sleep(1)

            step6 = "返回首页 返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="首页").click()
            # for i in range(4):
            #     SeaOfStarsAW.ut_device.swipe(0.025,0.5, 0.925,0.5)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')