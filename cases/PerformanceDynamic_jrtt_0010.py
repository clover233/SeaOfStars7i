import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jrtt_0010(Case):
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

            # 1、打开今日头条，启动3s
            logging.info('打开今日头条，启动3s')
            SeaOfStarsAW.trace_thread.add_log('今日头条', '启动今日头条，浏览主页')
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.article.News')
            time.sleep(3)
            # 2、主页浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览热榜')
            # 3、点击热搜tab，停留1s
            SeaOfStarsAW.ut_device(labelContains="热榜").click()
            time.sleep(1)

            # 4、滑动浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览发现页')
            # 5、点击热榜第一条，停留3s
            SeaOfStarsAW.ut_device.click(0.391, 0.332)
            time.sleep(3)

            # 6、滑动浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 7、侧滑一次，返回上一级，停留2s
            SeaOfStarsAW.ut_device(labelContains="返回").click()
            time.sleep(2)

            # 8、点击发现tab，停留1s
            SeaOfStarsAW.ut_device.click(0.454, 0.143)
            time.sleep(1)

            # 9、滑动浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览第一条文章')
            # 10、返回推荐页，点击第一条文章，停留1s
            SeaOfStarsAW.ut_device.click(0.2, 0.141)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.411, 0.23)
            time.sleep(1)

            # 11、滑动浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 12、返回首页，停留1s
            SeaOfStarsAW.ut_device(labelContains="返回").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(1)

            SeaOfStarsAW.trace_thread.add_log('今日头条', '返回桌面')
            # 13、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.article.News')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')