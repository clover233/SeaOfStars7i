import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jingdong_0040(Case):
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

            # 1、启动京东，等待3s
            logging.info('启动京东')
            SeaOfStarsAW.trace_thread.add_log('京东', '启动京东，等待3s')
            # todo 微博的坐标地址要改下
            # for _ in range(4):
            #     SeaOfStarsAW.swipe_left()
            #     time.sleep(2)
            # SeaOfStarsAW.ut_device.click(0.847, 0.246)
            # time.sleep(3)
            SeaOfStarsAW.ut_device.session().app_activate('com.360buy.jdmobile')
            time.sleep(3)
            time.sleep(2)

            # 2、点击底部直播，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击底部直播，浏览直播')
            SeaOfStarsAW.ut_device.click(0.625, 0.511)
            time.sleep(2)

            # 3、浏览直播页面，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、点击第一个直播间进去，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '进入直播间')
            SeaOfStarsAW.ut_device(labelContains="关注").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.264, 0.238)
            time.sleep(2)

            # 5、点击底部输入框，等待2s
            # 6、输入不错并发送，每次停留2s
            # SeaOfStarsAW.ut_device.click(0.213, 0.936)
            # time.sleep(2)
            # SeaOfStarsAW.ut_device().set_text("不错")
            # time.sleep(2)
            # SeaOfStarsAW.ut_device.click(0.883, 0.893)
            # time.sleep(2)

            # 7、点击右边购物袋，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击右边购物袋，浏览购物袋')
            SeaOfStarsAW.ut_device.click(0.918, 0.934)
            time.sleep(2)

            # 8、浏览购物袋，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 9、返回主页面，等待2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.8, 0.5, duration=0.03)
                time.sleep(2)

            # 10、点击我的，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击我的-全部订单-浏览')
            SeaOfStarsAW.ut_device(labelContains="我的").click()
            time.sleep(2)
            # SeaOfStarsAW.ut_device.click(0.5, 0.5)

            # 11、点击全部订单，等待2s
            SeaOfStarsAW.ut_device(label="全部").click()
            time.sleep(2)

            # 12、浏览全部订单页面，上滑2次，下滑2次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 13、点击待收货，停留2s
            SeaOfStarsAW.ut_device(labelContains="待收货").click()
            time.sleep(2)

            # 14、返回首页，等待2s
            SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.8, 0.5, duration=0.03)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)

            # 15、返回home页面，等待2s
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.360buy.jdmobile')
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')