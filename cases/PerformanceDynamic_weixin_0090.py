import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0090(Case):
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


            logging.info('启动微信')
            SeaOfStarsAW.trace_thread.add_log('微信', '启动微信')
            SeaOfStarsAW.ut_device.click(0.606, 0.585)
            logging.info('等待5s')
            time.sleep(5)
            SeaOfStarsAW.trace_thread.add_log('微信', '搜索华为手机')
            logging.info('点击搜索框')
            SeaOfStarsAW.ut_device.click(0.473, 0.125)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.93, 0.079)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '扫一扫')
            logging.info('点击右上角+号')
            SeaOfStarsAW.ut_device.click(0.933, 0.075)
            time.sleep(2)
            logging.info('点击扫一扫')
            SeaOfStarsAW.ut_device(label='扫一扫').click()
            time.sleep(2)
            logging.info('点击相册')
            SeaOfStarsAW.ut_device.click(0.883, 0.817)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '扫一扫相册浏览')
            logging.info('上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('侧滑返回')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            logging.info('侧滑返回首页')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '收付款')
            logging.info('点击右上角+号')
            SeaOfStarsAW.ut_device.click(0.933, 0.075)
            time.sleep(2)
            logging.info('点击收付款')
            SeaOfStarsAW.ut_device(label='收付款').click()
            time.sleep(2)
            logging.info('点击二维码收款')
            SeaOfStarsAW.ut_device(label='二维码收款').click()
            time.sleep(2)
            logging.info('侧滑返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回桌面')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')