import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xhs_0030(Case):
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

            step1 = "'打开小红书,等待10s'"
            logging.info('启动小红书')
            SeaOfStarsAW.trace_thread.add_log('小红书', step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.149, 0.714)
            time.sleep(10)

            step2 = "点击右上角 搜索"
            SeaOfStarsAW.trace_thread.add_log('小红书', step2)
            SeaOfStarsAW.ut_device.click(0.935, 0.085)
            time.sleep(1)

            step3 = "搜索 穿搭图片（停留1s）返回上一级 停留1s 重复3次"
            for i in range(3):
                SeaOfStarsAW.ut_device().set_text("穿搭图片")
                time.sleep(1)
                SeaOfStarsAW.ut_device.click(0.613, 0.474)
                time.sleep(1)

            step4 = "搜索 穿搭图片（停留1s）"
            SeaOfStarsAW.trace_thread.add_log('小红书', step4)
            SeaOfStarsAW.ut_device().set_text("穿搭图片")
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(1)

            step5 = "点击左上角第一条消息 停留1s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step5)
            SeaOfStarsAW.ut_device.click(0.247,0.347)
            time.sleep(1)

            step6 = "上滑一次  下滑一次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step6)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            step7 = "返回上一层 停留1s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step7)
            SeaOfStarsAW.ut_device(labelContains="返回").click()
            time.sleep(1)

            step8 = "上滑3次 下滑3次 重复2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step8)
            for i in range(2):
                for i in range(3):
                    SeaOfStarsAW.ut_device.swipe_up()
                for i in range(3):
                    SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step9 = "返回上一层"
            SeaOfStarsAW.trace_thread.add_log('小红书', step9)
            SeaOfStarsAW.ut_device(labelContains="返回").click()

            step10 = "点击搜索 下的 第一条热搜"
            SeaOfStarsAW.trace_thread.add_log('小红书', step10)
            SeaOfStarsAW.ut_device.click(0.463, 0.444)
            time.sleep(3)

            step11 = "上滑3次 下滑3次 重复2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step11)
            for i in range(2):
                for i in range(3):
                    SeaOfStarsAW.ut_device.swipe_up()
                for i in range(3):
                    SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step12 = "返回首页"
            SeaOfStarsAW.trace_thread.add_log('小红书', step12)
            SeaOfStarsAW.swipe_return()
            SeaOfStarsAW.swipe_return()

            step13 = "返回home页面"
            SeaOfStarsAW.trace_thread.add_log('小红书', step13)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')