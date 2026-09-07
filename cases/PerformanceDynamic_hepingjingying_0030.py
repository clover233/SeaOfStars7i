import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hepingjingying_0030(Case):
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

            # 1、启动和平精英，等待20s
            logging.info('启动和平精英，等待20s')
            SeaOfStarsAW.trace_thread.add_log('和平精英', '启动和平精英')
            SeaOfStarsAW.ut_device.session().app_activate('com.tencent.tmgp.pubgmhd')
            time.sleep(20)

            # 2、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.tencent.tmgp.pubgmhd')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')