import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_AutoNavi_0050(Case):
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
            SeaOfStarsAW.trace_thread.add_log('高德地图', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(7)
            SeaOfStarsAW.ut_device.click(0.497, 0.243, 0.50)
            time.sleep(1)

            # 2、地图界面上滑1次浏览（停留3s）
            logging.info('2、地图界面上滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '地图界面上滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(3)

            # 3、地图界面下滑1次浏览（停留3s）
            logging.info('3、地图界面下滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '地图界面下滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(3)

            # 4、地图界面左滑1次浏览（停留3s）
            logging.info('4、地图界面左滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '地图界面左滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(3)

            # 5、地图界面右滑1次浏览（停留3s）
            logging.info('5、地图界面右滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '地图界面右滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(3)

            # 6、双指捏合放大/缩小当前位置地图（停留3s）
            # 目前为双击放大，建议后期换成WDA的二指放大
            logging.info('6、双指捏合放大/缩小当前位置地图')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '双指捏合放大/缩小当前位置地图')
            SeaOfStarsAW.ut_device.double_tap(0.500, 0.500)
            time.sleep(3)

            # 7、左滑退出首页（停留1s）
            logging.info('7、左滑退出首页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '左滑退出首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 8、上滑返回桌面
            logging.info('8、上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.autonavi.amap')

        logging.info('用例执行结束')