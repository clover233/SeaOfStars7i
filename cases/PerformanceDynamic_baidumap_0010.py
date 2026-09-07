import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_baidumap_0010(Case):
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

            # 启动百度地图，停留2S
            # 建议停止5s 有广告
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.baidu.map')
            time.sleep(2)

            # 搜索框搜索钟楼，停留2S
            logging.info('2、搜索框搜索钟楼')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '搜索框搜索钟楼')
            SeaOfStarsAW.ut_device.click(0.241, 0.099, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("西安钟楼")
            SeaOfStarsAW.ut_device.click(0.890, 0.10, 0.5)
            time.sleep(2)

            # 选择西安钟楼，停留2S
            logging.info('3、选择西安钟楼')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '选择西安钟楼')
            SeaOfStarsAW.ut_device.click(0.454, 0.174, 0.5)
            time.sleep(2)

            # 点击到这去，停留2S
            logging.info('4、点击到这去')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '点击到这去')
            SeaOfStarsAW.ut_device.click(0.827, 0.939, 0.5)
            time.sleep(2)

            # 点击开始导航，停留2S
            logging.info('5、点击开始导航')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '点击开始导航')
            SeaOfStarsAW.ut_device.click(0.801, 0.943, 0.5)
            time.sleep(2)

            # 点击退出导航，停留2S
            logging.info('6、点击退出导航')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '点击退出导航')
            SeaOfStarsAW.ut_device.click(0.916, 0.933, 0.5)
            time.sleep(0.5)
            SeaOfStarsAW.ut_device.click(0.721, 0.941, 0.5)
            time.sleep(2)

            # 返回桌面
            logging.info('7、返回桌面')
            SeaOfStarsAW.trace_thread.add_log('百度地图', '返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.baidu.map')
            time.sleep(1)

        logging.info('用例执行结束')