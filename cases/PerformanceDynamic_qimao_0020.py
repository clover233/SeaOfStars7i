import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qimao_0020(Case):
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

            logging.info('启动七猫')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '启动七猫')
            SeaOfStarsAW.ut_device.click(0.163, 0.125)
            time.sleep(8)
            # SeaOfStarsAW.trace_thread.add_log('七猫', '主页浏览')
            logging.info('上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击发现')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '发现/热门浏览')
            SeaOfStarsAW.ut_device(label='发现').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击图书')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '图书浏览')
            SeaOfStarsAW.ut_device(label='图书').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击分类')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '言情浏览')
            SeaOfStarsAW.ut_device(label='分类').click()
            time.sleep(2)
            logging.info('点击现代言情')
            SeaOfStarsAW.ut_device(label='现代言情').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击最高评分')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '最高评分浏览')
            SeaOfStarsAW.ut_device(label='最高评分').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.076, 0.079)
            time.sleep(2)
            logging.info('点击书城')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '搜索书籍')
            SeaOfStarsAW.ut_device(label='书城').click()
            time.sleep(2)
            logging.info('点击搜索标志')
            SeaOfStarsAW.ut_device.click(0.463, 0.081)
            time.sleep(2)
            logging.info('输入长生')
            SeaOfStarsAW.ut_device.send_keys('长生')
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('点击返回')
            # SeaOfStarsAW.trace_thread.add_log('七猫', '返回桌面')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')