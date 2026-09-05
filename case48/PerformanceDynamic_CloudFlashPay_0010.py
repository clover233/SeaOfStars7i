import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_CloudFlashPay_0010(Case):
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
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动云闪付（3s）
            logging.info('1、启动云闪付')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '启动云闪付')
            SeaOfStarsAW.ut_device.session().app_activate('com.unionpay.chsp')
            time.sleep(3)

            # 2、主页浏览（上下各滑动1次，循环5次，每次停留2s）
            logging.info('2、主页浏览')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '主页浏览')
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 3、点击收付款（停留1s）
            logging.info('3、点击收付款')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '点击收付款')
            SeaOfStarsAW.ut_device.click(0.152, 0.183, 0.30)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 4、点击扫一扫（停留1s）
            logging.info('4、点击扫一扫')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '点击扫一扫')
            SeaOfStarsAW.ut_device.click(0.616, 0.179, 0.30)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 5、返回首页，点击扫一扫（停留1s）
            logging.info('5、返回首页，点击扫一扫')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '返回首页，点击扫一扫')
            SeaOfStarsAW.ut_device.click(0.616, 0.179, 0.30)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 6、点击优惠（停留1s）
            logging.info('6、点击优惠')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '点击优惠')
            SeaOfStarsAW.ut_device.click(0.306, 0.922, 0.30)
            time.sleep(1)
            # 7、浏览优惠页（上下各滑动1次，循环5次，每次停留2s）
            logging.info('7、浏览优惠页')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '浏览优惠页')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # # 8、点击惠生活（停留1s） 该页面没有了
            # logging.info('8、点击惠生活')
            # SeaOfStarsAW.trace_thread.add_log('云闪付', '点击惠生活')
            #
            # # 9、浏览惠生活（上下各滑动1次，循环5次，每次停留2s）
            # logging.info('9、浏览惠生活')
            # SeaOfStarsAW.trace_thread.add_log('云闪付', '浏览惠生活')
            #
            # # 10、返回上一层，点击享美食（停留1s）
            # logging.info('10、返回上一层，点击享美食')
            # SeaOfStarsAW.trace_thread.add_log('云闪付', '返回上一层，点击享美食')

            # 11、返回首页（停留1s）
            logging.info('11、返回首页')
            SeaOfStarsAW.trace_thread.add_log('云闪付', '返回首页')
            SeaOfStarsAW.ut_device.click(0.126, 0.924, 0.30)
            time.sleep(1)

            # 12、返回Home界面（停留1s）
            logging.info('12、返回Home界面')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回Home界面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.unionpay.chsp')
            time.sleep(1)

        logging.info('用例执行结束')