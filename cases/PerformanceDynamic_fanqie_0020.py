import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fanqie_0020(Case):
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

            # 1、启动番茄免费小说，启动3s
            logging.info('启动番茄免费小说，启动3s')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '启动番茄小说，浏览主页')
            SeaOfStarsAW.ut_device.session().app_activate('com.dragon.read')
            time.sleep(3)
            # 2、主页浏览，上滑3次，下滑3次，每次停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 3、点击听书，停留1s
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '听书浏览')
            SeaOfStarsAW.ut_device(labelContains="书城").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="听书").click()
            time.sleep(1)

            # 4、滑动浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 5、点击推荐，返回到首页
            SeaOfStarsAW.ut_device(labelContains="推荐").click()
            time.sleep(1)

            # 6、点击完本榜
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '完本榜浏览')
            SeaOfStarsAW.ut_device(labelContains="完本榜").click()
            time.sleep(1)
            # 7、左滑两次，右滑动两次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.759, 0.424, 0.374, 0.424, 0.5)
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.374, 0.424, 0.759, 0.424, 0.5)
            time.sleep(2)

            # 8、点击口碑榜，停留1s
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '口碑榜浏览')
            SeaOfStarsAW.ut_device.click(0.408, 0.207)
            time.sleep(1)
            # 9、左滑两次，右滑动两次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.759, 0.424, 0.374, 0.424, 0.5)
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.374, 0.424, 0.759, 0.424, 0.5)
            time.sleep(2)

            # 10、点击高分榜，停留1s
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '高风榜浏览')
            SeaOfStarsAW.ut_device.click(0.565, 0.206)
            time.sleep(1)
            # 11、左滑两次，右滑动两次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.759, 0.424, 0.374, 0.424, 0.5)
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.374, 0.424, 0.759, 0.424, 0.5)
            time.sleep(2)

            # 12、返回推荐榜，停留1s
            SeaOfStarsAW.ut_device(labelContains="完本榜").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="推荐榜").click()
            time.sleep(2)

            # 13、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.dragon.read')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')