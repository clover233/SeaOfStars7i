import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_taobao_0020(Case):
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
            # step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)


            logging.info('启动淘宝')
            # # SeaOfStarsAW.trace_thread.add_log('QQ', '应用启动')
            SeaOfStarsAW.ut_device.app_activate('com.taobao.taobao4iphone')
            logging.info('等待5s')
            time.sleep(5)
            logging.info('进入第三个tab页')
            SeaOfStarsAW.ut_device.click(0.316, 0.069)
            time.sleep(2)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('进入推荐页')
            # SeaOfStarsAW.ut_device(label='推荐').click()
            # SeaOfStarsAW.ut_device.xpath('//*[@label="推荐，未选中"]').click()
            SeaOfStarsAW.ut_device.click(0.19, 0.069)
            time.sleep(2)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('进入关注页')
            # SeaOfStarsAW.ut_device(label='关注').click()
            SeaOfStarsAW.ut_device.click(0.073, 0.066)
            time.sleep(2)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('左滑3次，右滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)
            SeaOfStarsAW.ut_device(label='我的淘宝').click()
            time.sleep(2)
            logging.info('点击我的订单')
            SeaOfStarsAW.ut_device.click(0.106, 0.336)
            time.sleep(2)
            logging.info('左滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            logging.info('右滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)
            logging.info('点击返回首页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')