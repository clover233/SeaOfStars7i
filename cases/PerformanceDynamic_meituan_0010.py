import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_meituan_0010(Case):
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

            # 1、启动美团，停留3s
            logging.info('启动美团，等待3s')
            SeaOfStarsAW.trace_thread.add_log('美团', '进入外卖美食')
            SeaOfStarsAW.ut_device.session().app_activate('com.meituan.imeituan')
            time.sleep(3)

            # 2、首页点击外卖，停留1s
            SeaOfStarsAW.ut_device(labelContains="外卖").click()
            time.sleep(2)

            # 3、点击美食，停留1s
            SeaOfStarsAW.ut_device(labelContains="美食").click()
            time.sleep(2)

            # 4、点击搜索框，停留1s
            SeaOfStarsAW.trace_thread.add_log('美团', '搜索美食')
            SeaOfStarsAW.ut_device.click(0.219, 0.148)
            time.sleep(1)

            # 5、输入黄焖鸡，停留1s
            SeaOfStarsAW.ut_device.click(0.331, 0.081)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys('黄焖鸡')
            time.sleep(2)

            # 6、点击搜索，停留1s
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 7、滑动浏览，上滑5次，下滑5次，停留2s
            SeaOfStarsAW.trace_thread.add_log('美团', '浏览美食')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 8、点击第一家店铺，停留1s
            SeaOfStarsAW.trace_thread.add_log('美团', '加入购物车')
            SeaOfStarsAW.ut_device.click(0.431, 0.41)
            time.sleep(1)

            # 9、上下各滑动1次浏览店家，停留1s
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 10、点击评价，上次各滑动2次，浏览评价
            SeaOfStarsAW.ut_device.click(0.286, 0.148)
            time.sleep(1)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 11、返回进入点菜界面，停留1s
            SeaOfStarsAW.ut_device.click(0.074, 0.146)
            time.sleep(1)

            # 12、点击推荐下的第一份食品，停留1s
            SeaOfStarsAW.ut_device.click(0.381, 0.321)
            time.sleep(1)

            # 13、点击加入购物车，停留1s
            SeaOfStarsAW.ut_device(labelContains="加入购物车").click()
            time.sleep(1)

            # 14、再次点击加入购物车，停留1s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 15、点击购物车图标，停留1s
            # 16、侧滑返回美食界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('美团', '浏览美食')
            # 17、滑动浏览美食，上滑2次，下滑2次，停留2s
            # 18、返回美团首页，停留1s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 19、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.meituan.imeituan')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')