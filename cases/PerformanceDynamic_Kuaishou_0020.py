import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Kuaishou_0020(Case):
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

            # 1、点击进入快手，启动5s，等待2s
            logging.info('启动快手，等待5s')
            SeaOfStarsAW.trace_thread.add_log('快手', '浏览搜索结果')
            SeaOfStarsAW.ut_device.session().app_activate('com.jiangjia.gif')
            time.sleep(5)

            # 2、点击首页右上角搜索图标，1s
            SeaOfStarsAW.ut_device.click(0.919, 0.095)
            time.sleep(1)

            # 3、搜索“华为手机”，停留2s
            SeaOfStarsAW.ut_device.click(0.28, 0.096)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 4、上滑3次，下滑3次，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 5、返回搜索页
            SeaOfStarsAW.ut_device.swipe_right()

            # 6、点击直播榜，1s
            SeaOfStarsAW.trace_thread.add_log('快手', '启动进入直播榜')
            SeaOfStarsAW.ut_device(labelContains="直播榜").click()
            time.sleep(2)

            # 7、点击排名第一的直播账号，查看直播15s
            SeaOfStarsAW.trace_thread.add_log('快手', '观看直播')
            SeaOfStarsAW.ut_device.click(0.351, 0.589)
            time.sleep(15)

            # 8、上滑查看下一个直播，15s
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(15)

            # 9、左滑3次返回首页
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            # 10、上滑返回桌面
            SeaOfStarsAW.ut_device.app_terminate('com.jiangjia.gif')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')