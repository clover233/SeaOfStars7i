import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_tielu12306_0020(Case):
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

            logging.info('启动铁路12306')
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '启动12306')
            SeaOfStarsAW.ut_device.click(0.843, 0.697)
            logging.info('等待1s')
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '首页抛滑3次')
            logging.info('上滑3次')   # 抛滑暂用swipe代替
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '首页点击酒店')
            logging.info('点击任一酒店')
            SeaOfStarsAW.ut_device.click(0.246, 0.519)
            time.sleep(2)
            logging.info('返回上一页')
            SeaOfStarsAW.ut_device.click(0.046, 0.076)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '切换底部tab')
            logging.info('点击出行服务')
            SeaOfStarsAW.ut_device(label='出行服务').click()
            time.sleep(1)
            logging.info('点击订单')
            SeaOfStarsAW.ut_device(label='订单').click()
            time.sleep(1)
            logging.info('点击铁路会员')
            SeaOfStarsAW.ut_device(label='铁路会员').click()
            time.sleep(1)
            logging.info('点击首页')
            SeaOfStarsAW.ut_device(label='首页').click()
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('铁路12306', '首页浏览，下滑2次')
            logging.info('下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('退出桌面')
            # SeaOfStarsAW.trace_thread.add_log('12306', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')