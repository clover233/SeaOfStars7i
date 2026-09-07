import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_AutoNavi_0030(Case):
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
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(2)
        for test_time in range(0, self.TEST_TIME):
            step = 0

            # 1、点击高德地图(温启2s，停留2s)
            logging.info('1、点击高德地图')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击高德地图')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(2)

            # 2、搜索“西安北站”(停留1s)
            logging.info('2、搜索西安北站')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '搜索西安北站')
            SeaOfStarsAW.ut_device.click(0.922, 0.475, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.298, 0.138, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("西安北站")
            time.sleep(1)

            # 3、切换到“公交地铁”（1s）
            logging.info('3、切换到“公交地铁”')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '切换到“公交地铁”')
            SeaOfStarsAW.ut_device.click(0.465, 0.293, 0.10)
            time.sleep(1)

            # 4、上滑3次，下滑4次，等待2秒
            logging.info('4、向上滑3次')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向上滑3次')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('4、向下滑4次')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向下滑4次')
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 5、点击第一条路线，上滑1次，下滑1次
            logging.info('5、点击第一条路线，上滑1次，下滑1次')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击第一条路线，上滑1次，下滑1次')
            SeaOfStarsAW.ut_device.click(0.488, 0.389, 0.10)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            # 6、返回首页
            logging.info('6、返回首页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回首页')
            for i in range(2):
                SeaOfStarsAW.ut_device.click(0.071, 0.103, 0.10)
                time.sleep(1)

            # 7、上滑返回桌面
            logging.info('7、上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.autonavi.amap')

        logging.info('用例执行结束')