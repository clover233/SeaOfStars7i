import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0080(Case):
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
            SeaOfStarsAW.trace_thread.add_log('微信', '测试账号拍摄')
            logging.info('点击测试账号，暂定文件传输助手')
            SeaOfStarsAW.ut_device(label='文件传输助手').click()
            time.sleep(2)
            logging.info('点击加号')
            SeaOfStarsAW.ut_device.click(0.943, 0.932)
            time.sleep(2)
            logging.info('点击拍摄')
            SeaOfStarsAW.ut_device(label='拍摄').click()
            time.sleep(2)
            logging.info('点击拍摄按钮')
            SeaOfStarsAW.ut_device.click(0.493, 0.892)
            time.sleep(2)
            logging.info('点击发送')
            SeaOfStarsAW.ut_device.click(0.866, 0.892)
            time.sleep(2)
            logging.info('点击拍摄')
            SeaOfStarsAW.trace_thread.add_log('微信', '测试账号录像')
            SeaOfStarsAW.ut_device(label='拍摄').click()
            time.sleep(2)
            logging.info('长按开始录像')
            SeaOfStarsAW.ut_device.tap_hold(0.5, 0.894,5)
            time.sleep(2)
            logging.info('点击发送')
            SeaOfStarsAW.ut_device.click(0.866, 0.892)
            time.sleep(2)
            logging.info('点击照片')
            SeaOfStarsAW.ut_device(label='照片').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '测试账号浏览照片')
            logging.info('上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击选择第一张照片')
            SeaOfStarsAW.ut_device.click(0.2, 0.122)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '测试发送照片')
            logging.info('点击发送')
            SeaOfStarsAW.ut_device.click(0.876, 0.935)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '返回桌面')
            logging.info('侧滑返回')
            SeaOfStarsAW.ut_device.click(0.046, 0.075)
            time.sleep(2)
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)




        logging.info('用例执行结束')