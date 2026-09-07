import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_AutoNavi_0040(Case):
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

            # 1、启动高德地图（停留7s）
            logging.info('1、应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(7)

            # 2、点击搜索框（停留5s）
            logging.info('2、点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击搜索框')
            SeaOfStarsAW.ut_device.click(0.238, 0.557, 0.20)
            time.sleep(5)

            # 3、点击美食，等待3秒
            logging.info('3、点击美食')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击美食')
            SeaOfStarsAW.ut_device.click(0.109, 0.162, 0.20)
            time.sleep(3)

            # 4、上滑3次浏览美食，每次间隔1秒
            logging.info('4、上滑3次浏览美食')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑3次浏览美食')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 5、下滑3次浏览美食，每次间隔1秒
            logging.info('5、下滑3次浏览美食')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '下滑3次浏览美食')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 6、点击第一条搜索结果（停留7s）
            logging.info('6、点击第一条搜索结果')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击第一条搜索结果')
            SeaOfStarsAW.ut_device.click(0.554, 0.376, 0.20)
            time.sleep(7)

            # 7、点击路线（停留5s）
            logging.info('7、点击路线')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击路线')
            SeaOfStarsAW.ut_device.click(0.853, 0.928, 0.20)
            time.sleep(5)

            # 8、点击开始导航（停留7s）
            logging.info('8、点击开始导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击开始导航')
            SeaOfStarsAW.ut_device.click(0.632, 0.943, 0.20)
            time.sleep(7)

            # 9、向右滑动（停留3s）
            logging.info('9、向右滑动')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向右滑动')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(3)

            # 10、点击退出导航（停留3s）
            logging.info('10、点击退出导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击退出导航')
            SeaOfStarsAW.ut_device.click(0.103, 0.923, 0.20)
            time.sleep(0.2)
            SeaOfStarsAW.ut_device.click(0.258, 0.927, 0.20)
            time.sleep(3)

            # 11、上滑返回桌面（停留1s）
            logging.info('11、上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.autonavi.amap')

        logging.info('用例执行结束')