import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_youku_0020(Case):
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
            app_name ="优酷"

            step1 = "'1、打开优酷,等待10s'"
            logging.info('启动优酷')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.388, 0.144)
            time.sleep(10)

            step2 = "2、点击剧集 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="剧集").click()
            time.sleep(2)

            step3 = "3、浏览 上滑5次 下滑5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step4 = "4、点击电影"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="电影").click()
            time.sleep(5)

            step5 = "5、浏览 上滑5次 下滑5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step6 = "6、点击综艺"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="综艺").click()

            step7 = "7、浏览 上滑5次 下滑5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step8 = "8、点击搜索框"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.556, 0.084)

            step9 = "9、搜索好声音"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device().set_text("好声音")
            SeaOfStarsAW.ut_device(label="搜索").click()


            step10 = "10、浏览 上滑5次 下滑5次 每次停留2s 并切换横竖屏"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step11 = "11、返回主界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device().set_text("取消")
            SeaOfStarsAW.ut_device().set_text("取消")


            step12 = "12、左滑返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device(label="首页").click()


            step15 = "13、返回home 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

        logging.info('用例执行结束')