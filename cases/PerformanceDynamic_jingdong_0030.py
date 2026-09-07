import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jingdong_0030(Case):
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

            # 2、点击搜索框，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击搜索框，等待2s')
            SeaOfStarsAW.ut_device.click(0.374, 0.136)
            time.sleep(2)

            # 3、搜索华为手机，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '搜索华为手机，等待2s')
            SeaOfStarsAW.ut_device().set_text("华为手机")
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 4、搜索结果页浏览，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '搜索结果页浏览，上滑5次，下滑5次，每次停留2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(7):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 5、点击顶部销量，等待2s
            SeaOfStarsAW.ut_device.click(0.7, 0.653)
            time.sleep(2)
            # 6、点击第一个商品进入详情页，每次停留2s
            SeaOfStarsAW.ut_device.click(0.184, 0.897)
            time.sleep(2)

            # 7、浏览详情页，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '浏览详情页，上滑5次，下滑5次，每次停留2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(7):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 8、点击商品图片，停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击商品图片，停留2s')
            SeaOfStarsAW.ut_device(labelContains="图集").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.473, 0.23)
            time.sleep(2)

            # 9、滑动浏览，左滑3次，右滑3次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '滑动浏览，左滑3次，右滑3次，每次停留2s')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 10、侧滑返回商品详情页
            SeaOfStarsAW.trace_thread.add_log('京东', '侧滑返回商品详情页')
            SeaOfStarsAW.ut_device.click(0.054, 0.073)
            time.sleep(2)

            # 11、上滑至评价
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            # 12、点击评价，停留2s
            SeaOfStarsAW.ut_device.click(0.253, 0.082)
            time.sleep(2)

            # 13、点击全部评价，停留2s
            SeaOfStarsAW.ut_device.click(0.782, 0.127)
            time.sleep(2)

            # 14、浏览全部评价，上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '浏览全部评价，上滑3次，下滑3次，每次停留2s')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 15、点击左下角店铺，停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击左下角店铺，停留2s')
            SeaOfStarsAW.ut_device(labelContains="店铺").click()
            time.sleep(2)

            # 16、浏览店铺，上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('京东', '浏览店铺，上滑3次，下滑3次，每次停留2s')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 17、返回商品详情页面，等待2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 18、点击客服，等待2s
            SeaOfStarsAW.ut_device(labelContains="客服").click()
            time.sleep(2)

            # 19、返回商品详情页面，等待2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 20、点击立即购买，等待2s
            SeaOfStarsAW.ut_device.click(0.801, 0.937)
            time.sleep(2)

            # 21、点击确认，等待2s

            # 22、返回首页，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '返回首页等待2s')
            SeaOfStarsAW.ut_device.click(0.936, 0.102)
            time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            # 23、返回home页，等待2s
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.360buy.jdmobile')
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')