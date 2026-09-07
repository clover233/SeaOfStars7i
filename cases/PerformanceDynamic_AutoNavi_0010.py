import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_AutoNavi_0010(Case):
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
        # 清空后台


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
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、打开高德地图 (启动5s，可能有广告，停留2s)
            logging.info('1、打开高德地图')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '打开高德地图')
            SeaOfStarsAW.ut_device.app_activate("com.autonavi.amap")
            time.sleep(5)
            time.sleep(2)

            # 2、点击搜索框，点击“西安北站(北进站口)”记录(停留1s) 所以要之前搜索过西安北站(北进站口)，且该记录在第一名
            logging.info('2、点击搜索框，点击“西安北站(北进站口)”记录')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击搜索框，点击“西安北站(北进站口)”记录')
            SeaOfStarsAW.ut_device.click(0.261, 0.557, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.29, 0.408, 0.20)
            time.sleep(1)

            # 3、点击路线，点击驾车，点击开始导航（10s）
            logging.info('3、点击路线，点击驾车，点击开始导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击路线，点击驾车，点击开始导航')
            SeaOfStarsAW.ut_device.click(0.847, 0.926, 0.5)
            time.sleep(1)
            # 若处在驾车状态
            # SeaOfStarsAW.ut_device.click(0.054, 0.174, 0.20)
            # time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.701, 0.94, 0.20)

            # 4、停留10s
            logging.info('4、停留10s')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '停留10s')
            time.sleep(10)

            # 5、右滑退出（停留1s）
            logging.info('5、右滑退出')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '右滑退出')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 6、点击退出导航（停留1s）
            logging.info('6、点击退出导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击退出导航')
            SeaOfStarsAW.ut_device.click(0.109, 0.922, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.255, 0.926, 0.20)
            time.sleep(1)

            # 7、返回高德首页面(停留1s)
            logging.info('7、返回高德首页面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回高德首页面')
            SeaOfStarsAW.ut_device.click(0.054, 0.099, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.054, 0.099, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.054, 0.099, 0.20)
            time.sleep(1)

            # 8、返回home页面(停留1s)
            logging.info('8、返回home页面(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回home页面(停留1s)')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.autonavi.amap')
            time.sleep(1)
        logging.info('用例执行结束')