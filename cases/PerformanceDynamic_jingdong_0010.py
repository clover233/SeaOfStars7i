import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jingdong_0010(Case):
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

            # 2、首页浏览，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '首页浏览，上滑5次，下滑5次，每次停留2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 3、点击顶部手机数码，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击顶部手机数码，等待2s-浏览')
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.518, 0.183)
            time.sleep(2)
            # 4、手机数码界面浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、点击底部分类，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '击底部分类，等待2s-浏览')
            SeaOfStarsAW.ut_device.click(0.097, 0.934)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.878, 0.425)
            time.sleep(2)
            # 6、分类页面浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 7、点击左侧电脑，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击左侧电脑，等待2s-浏览')
            SeaOfStarsAW.ut_device.click(0.241, 0.218)
            time.sleep(2)
            # 8、电脑页面浏览，上滑5次、下滑5次，等待2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 9、点击第一类商品进入，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击第一类商品进入，等待2s-浏览')
            SeaOfStarsAW.ut_device.click(0.16, 0.351)
            time.sleep(2)
            # 10、浏览商品页，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 11、返回首页等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '返回首页等待2s')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            # 12、返回home页，等待2s
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.360buy.jdmobile')
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')