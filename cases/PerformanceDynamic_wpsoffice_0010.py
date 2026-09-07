import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_wpsoffice_0010(Case):
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

            step2 = "2、首页 左右各滑动1次 重复5次 每次间隔1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0.025,0.5, 0.925,0.5)
                time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0.925,0.5,0.025,0.5)
                time.sleep(1)

            step3 = "3、点击底部 云文档icon 点击首页 icon 重复5次 每次间隔1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(5):
                SeaOfStarsAW.ut_device(label="文档").click()
                time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device(label="首页").click()
                time.sleep(1)

            step4 = "4、点击 我 icon 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="我").click()

            step5 = "5、点击设置 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)

            SeaOfStarsAW.ut_device.swipe_down()
            SeaOfStarsAW.ut_device(label="设置").click()
            time.sleep(1)


            step6 = "6、侧滑一次 返回 我 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.swipe(0.025, 0.5, 0.925, 0.5)
            time.sleep(1)

            # step7 = "点击超级会员  进入支付界面 停留2s"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            # SeaOfStarsAW.ut_device(label="返回按钮").click()
            # time.sleep(2)
            #
            # step8 = "右滑返回上一级界面 停留2s"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            # SeaOfStarsAW.ut_device(label="购买按钮").click()
            # time.sleep(2)

            step9 = "点击 首页 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            # SeaOfStarsAW.ut_device(label="去购物车").click()
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)

            step10 = "点击 文档 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device(label="文档").click()
            time.sleep(2)

            # step11 = "上下滑动文档 重复5次 每次间隔1s"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            # SeaOfStarsAW.ut_device(label="返回按钮").click()
            # SeaOfStarsAW.ut_device.click(0.371, 0.586)
            # time.sleep(2)
            #
            # step12 = "侧滑返回首页"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            # SeaOfStarsAW.ut_device.swipe(0.778,0.315,0.578,0.315)
            # time.sleep(1)


            step13 = "返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')