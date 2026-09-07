import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Dingding_0020(Case):
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

            step2 = "2、点击更多"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="更多").click()

            step3 = "3、点击会议 切换到会议详情界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device(label="会议").click()

            time.sleep(1)

            step4 = "4、点击发起会议 点击语音会议"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="发起会议").click()
            SeaOfStarsAW.ut_device(label="语音会议").click()
            time.sleep(1)

            step5 = "5、点进 进入会议"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device(label="进入会议").click()
            time.sleep(1)

            step6 = "6、上滑退出到桌面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step7 = "7、打开今日头条 3s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device.click(0.383, 0.606, 0.3)
            time.sleep(6)

            step8 = "8、主页浏览 上下各滑动5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step9 = "9、点击 热榜 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device(label="热榜").click()
            time.sleep(1)

            step10 = "10、上下各滑动5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step11 = "11、打开第一条 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.click(0.422, 0.278, 0.3)
            time.sleep(2)

            step12 = "12、上下各滑动5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step13 = "13、返回 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.click(0.056, 0.104, 0.3)
            time.sleep(1)

            step14 = "14、点击 发现 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device(label="推荐").click()
            time.sleep(1)

            step15 = "15、上下各滑动5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step16 = "16、返回推荐页面 点击第一条 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            SeaOfStarsAW.ut_device.click(0.422, 0.278, 0.3)
            time.sleep(1)

            step17 = "17、上下各滑动5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step18 = ("18、返回首页 1s")
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            SeaOfStarsAW.ut_device.click(0.056, 0.104)
            time.sleep(1)

            step19 = "19、返回home 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step19)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step20 = "20、打开钉钉 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step20)
            SeaOfStarsAW.ut_device.click(0.384, 0.367)
            time.sleep(10)

            step21 = "21、点击 今日列表中的第一个会议  点击 入会"
            SeaOfStarsAW.trace_thread.add_log(app_name, step21)

            time.sleep(10)

            step22 = "22、等待60s后 点击结束 点击全员结束会议 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step22)
            time.sleep(60)
            SeaOfStarsAW.ut_device(label="结束").click()


            step23 = "23、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step23)
            SeaOfStarsAW.ut_device(label="工作台").click()

            step24 = "24、返回桌面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step24)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)


        logging.info('用例执行结束')