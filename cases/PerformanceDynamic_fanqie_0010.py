import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fanqie_0010(Case):
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
            # 1、启动番茄免费小说，启动3s
            logging.info('启动番茄免费小说，启动3s')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '启动番茄小说，浏览主页')
            SeaOfStarsAW.ut_device.session().app_activate('com.dragon.read')
            time.sleep(3)
            # 2、主页浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 3、点击书架，停留1s
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '查看书架书籍，阅读书籍')
            SeaOfStarsAW.ut_device(labelContains="书架").click()
            time.sleep(1)
            # 4、点击书籍进行阅读，停留1s
            for j in range(2):
                SeaOfStarsAW.ut_device.click(0.16, 0.246)
                time.sleep(1)
            # 5、阅读书籍，向左翻页5次，向右翻页5次，1s，停留3s
                for i in range(5):
                    SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(3)
                for i in range(5):
                    SeaOfStarsAW.ut_device.swipe(0.329, 0.504, 0.699, 0.504, duration=0.3)
                time.sleep(3)

            # 6、重复操作4、5步骤两次
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(1)
            # 7、返回首页，停留1s

            # 8、点击我的，停留1s
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '查看浏览历史')
            SeaOfStarsAW.ut_device(labelContains="我的").click()
            time.sleep(1)
            # 9、点击浏览历史，停留1s
            SeaOfStarsAW.ut_device(labelContains="浏览历史").click()
            time.sleep(2)

            # 10、返回首页，停留1s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="书城").click()
            time.sleep(1)
            # 11、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.dragon.read')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')