import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_zhihu_0030(Case):
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
            app_name ="知乎"

            step1 = "'1、打开知乎,等待10s'"
            logging.info('启动知乎')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.626, 0.133)
            time.sleep(10)

            step2 = "2、点击推荐 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(label="推荐").click()
            time.sleep(1)

            step3 = "3、浏览 上滑2次 下滑动3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step4 = "4、点击热榜 停留1"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="热榜").click()
            time.sleep(1)

            step5 = "5、浏览 上滑2次 下滑动3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step6 = "6、点击热榜第一条 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.54, 0.307)
            time.sleep(1)

            step7 = "7、浏览 上滑2次 下滑动3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step8 = "8、点击 第一条文章 查看信息 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.582, 0.546)
            time.sleep(1)

            step9 = "9、浏览 上滑2次 下滑动3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            step10 = "10、点击右下角评论 停留1"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device(label="评论").click()
            time.sleep(1)

            step11 = "11、浏览 上滑2次 下滑动3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step12 = "12、返回推荐界面 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device(label="返回").click()
            SeaOfStarsAW.ut_device(label="返回").click()
            SeaOfStarsAW.ut_device(label="推荐").click()
            time.sleep(2)

            step13 = "13、搜索一组桌面壁纸 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.click(0.562, 0.082)
            SeaOfStarsAW.ut_device().set_text("桌面壁纸")
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)

            step14 = "14、点击 第一条结果 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device.click(0.252, 0.38)
            time.sleep(1)

            step15 = "15、点击图片 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.click(0.282, 0.334)
            time.sleep(1)

            step16 = "16、左滑2次 右滑2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            step17 = "17、返回首页 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.click(0.252, 0.38)
            SeaOfStarsAW.ut_device.click(0.93, 0.097)
            SeaOfStarsAW.ut_device.click(0.05, 0.009)
            SeaOfStarsAW.ut_device.click(0.05, 0.009)

            time.sleep(2)

            step18 = "18、点击底部  发现 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(1)

            step19 = "19、点击底部 首页 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step19)
            SeaOfStarsAW.ut_device(label="发现").click()
            time.sleep(2)

            step20 = "20、返回home 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step20)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)


        logging.info('用例执行结束')