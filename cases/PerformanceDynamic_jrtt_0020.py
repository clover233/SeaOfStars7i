import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jrtt_0020(Case):
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
            SeaOfStarsAW.trace_thread.add_log('今日头条', '启动今日头条，搜索图片')
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.article.News')
            time.sleep(3)
            # 2、搜索“图片”，停留2s
            SeaOfStarsAW.ut_device.click(0.324, 0.093)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys("图片")
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.528, 0.147)
            time.sleep(2)

            # 3、点击搜索结果第一条图片进行预览，停留2s
            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览搜索结果')
            SeaOfStarsAW.ut_device.click(0.24, 0.29)
            time.sleep(2)

            # 4、滑动浏览，左滑5次，右滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0.329, 0.504, 0.699, 0.504, duration=0.3)
                time.sleep(2)

            # 5、侧滑3次，返回到首页
            SeaOfStarsAW.ut_device.click(0.121, 0.934)
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device(labelContains="返回").click()
                time.sleep(1)

            # 6、点击视频
            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览视频')
            SeaOfStarsAW.ut_device.click(0.372, 0.926)
            time.sleep(2)

            # 7、滑动浏览视频，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 8、点击评论按钮
            SeaOfStarsAW.trace_thread.add_log('今日头条', '浏览评论')
            SeaOfStarsAW.ut_device.click(0.933, 0.581)
            time.sleep(1)

            # 9、滑动浏览评论，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 10、返回首页，停留1s
            SeaOfStarsAW.ut_device.click(0.926, 0.333)
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(1)

            # 11、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.article.News')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')