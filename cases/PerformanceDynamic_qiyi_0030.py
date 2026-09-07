import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qiyi_0030(Case):
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

            logging.info('启动爱奇艺')
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '启动爱奇艺')
            SeaOfStarsAW.ut_device.click(0.843, 0.701)
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '首页浏览')
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '浏览播放视频')
            logging.info('点击主页第1个推荐视频')  # 注意有广告情况)
            SeaOfStarsAW.ut_device.click(0.256, 0.559)
            time.sleep(10)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('上滑退出')
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')