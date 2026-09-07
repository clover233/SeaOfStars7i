import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xiechengTrip_0010(Case):
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

            step2 = "2、上 抛滑1次 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step3 = "3、下 抛滑1次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step4 = "4、点击民宿 客栈 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="民宿/客栈").click()

            step5 = "5、向上抛滑2次  每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step6 = "6、向下抛滑3次  每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step7 = "7、点击查询按钮"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device.click(0.512, 0.505)

            step8 = "8、输入 臻选民宿 点击搜索"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.476, 0.088)
            SeaOfStarsAW.ut_device().set_text("臻选民宿")
            SeaOfStarsAW.ut_device(label="搜索").click()

            step9 = "9、点击第一个民宿"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device.click(0.53, 0.464)


            step10 = "10、向上抛滑2次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step11 = "11、点击评论 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device(label="评价").click()

            step12 = "12、点击查看75条评论"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.72, 0.337)

            step13 = "13、上滑2次 下滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step14 = "14、左滑1次 返回"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)

            step15 = "15、点击全部设施"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device(label="设施").click()

            step16 = "16、向下 抛滑3次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()


            step17 = "17、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)

            step18 = "18、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')