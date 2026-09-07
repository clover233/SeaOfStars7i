import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_meituan_0090(Case):
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

            # 1、启动美团（停留3s）
            logging.info('启动美团，等待3s')
            SeaOfStarsAW.trace_thread.add_log('美团', '进入外卖美食')
            SeaOfStarsAW.ut_device.session().app_activate('com.meituan.imeituan')
            time.sleep(3)

            # 2、首页滑动浏览（上滑5次，每次停留2s）
            logging.info('2、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 3、首页滑动浏览（下滑5次，每次停留2s）
            logging.info('3、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('美团', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、点击美食团购（停留1s）
            logging.info('4、点击美食团购')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击美食团购')
            SeaOfStarsAW.ut_device.click(0.309, 0.191, 0.50)
            time.sleep(1)

            # 5、滑动浏览美食团购页面（上滑2次，下滑2次，每次停留2s）
            logging.info('上滑2次，下滑2次')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑5次')
            time.sleep(1)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('美团', '下滑2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 6、返回美团首页面，2s
            logging.info('6、返回美团首页面')
            SeaOfStarsAW.trace_thread.add_log('美团', '返回美团首页面')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 7、点击“休闲玩乐”，2s
            logging.info('7、点击“休闲玩乐”')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击“休闲玩乐”')
            SeaOfStarsAW.ut_device.click(0.501, 0.268, 0.50)
            time.sleep(2)

            # 8、点击第一条结果，2s
            logging.info('8、点击第一条结果')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击第一条结果')
            SeaOfStarsAW.ut_device.click(0.541, 0.581, 0.30)
            time.sleep(2)

            # 9、上滑2次，下滑2次，等待2s
            logging.info('9、上滑2次，下滑2次')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑5次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('美团', '下滑2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 10、返回主界面，2s
            logging.info('10、返回主界面')
            SeaOfStarsAW.trace_thread.add_log('美团', '返回主界面')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 11.点击外卖（停留1s）
            logging.info('11.点击外卖')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击外卖')
            SeaOfStarsAW.ut_device.click(0.12, 0.192, 0.50)
            time.sleep(1)

            # 12 点击搜索框 （停留2秒）
            logging.info('12、点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击搜索框')
            SeaOfStarsAW.ut_device.click(0.183, 0.127, 0.50)
            time.sleep(2)

            # 13 输入“24小时药店”（停留2秒）
            logging.info('13 输入“24小时药店”')
            SeaOfStarsAW.trace_thread.add_log('美团', '输入“24小时药店”')
            SeaOfStarsAW.ut_device().set_text("24小时药店")
            time.sleep(2)

            # 14 点击搜索（停留3秒）
            logging.info('14 点击搜索')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击搜索')
            SeaOfStarsAW.ut_device.click(0.868, 0.084, 0.50)
            time.sleep(3)

            # 15.点击第一个商家（停留2s）
            logging.info('15.点击第一个商家（停留2s）')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击第一个商家（停留2s）')
            SeaOfStarsAW.ut_device.click(0.481, 0.349, 0.50)
            time.sleep(2)

            # 16.点击+（停留1s）
            logging.info('16.点击+')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击+')
            SeaOfStarsAW.ut_device.click(0.934, 0.563, 0.50)
            SeaOfStarsAW.ut_device.click(0.936, 0.673, 0.50)
            time.sleep(1)

            # 17.点击加入购物车（停留1s）
            logging.info('17.点击加入购物车')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击加入购物车')
            SeaOfStarsAW.ut_device.click(0.203, 0.963, 0.20)
            time.sleep(1)

            # 18.清空购物车（停留2s）
            logging.info('18.清空购物车')
            SeaOfStarsAW.trace_thread.add_log('美团', '清空购物车')
            SeaOfStarsAW.ut_device.click(0.873, 0.791, 0.20)
            time.sleep(2)

            # 19.返回到外卖界面（停留2s）
            logging.info('19.返回到外卖界面')
            SeaOfStarsAW.trace_thread.add_log('美团', '返回到外卖界面')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.048, 0.084, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 20.点击我的（停留2s）
            logging.info('20.点击我的')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击我的')
            SeaOfStarsAW.ut_device.click(0.882, 0.934, 0.50)
            time.sleep(2)

            # 21.点击我的地址（停留2s）
            logging.info('21.点击我的地址')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击我的地址')
            SeaOfStarsAW.ut_device.click(0.928, 0.104, 0.50)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.512, 0.223, 0.20)
            time.sleep(2)

            # 22.点击第一个收货地址（停留2s）
            logging.info('22.点击第一个收货地址')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击第一个收货地址')
            SeaOfStarsAW.ut_device.click(0.902, 0.168, 0.20)
            time.sleep(2)

            # 23.点击保存地址（停留2s）
            logging.info('23.点击保存地址')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击保存地址')
            SeaOfStarsAW.ut_device.click(0.495, 0.594, 0.20)
            time.sleep(2)

            # 24.点击新增收货地址（停留2s）
            logging.info('24.点击新增收货地址')
            SeaOfStarsAW.trace_thread.add_log('美团', '点击新增收货地址')
            SeaOfStarsAW.ut_device.click(0.871, 0.088, 0.20)
            time.sleep(2)

            # 25.返回首页（停留1s）
            logging.info('25.返回首页')
            SeaOfStarsAW.trace_thread.add_log('美团', '返回首页')
            SeaOfStarsAW.ut_device.click(0.04, 0.086, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.04, 0.086, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.04, 0.086, 0.20)
            time.sleep(1)

            # 26.上滑返回home界面（停留1s）
            logging.info('26.上滑返回home界面')
            SeaOfStarsAW.trace_thread.add_log('美团', '上滑返回home界面')
            SeaOfStarsAW.swipe_to_launcher()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.meituan.imeituan')

        logging.info('用例执行结束')