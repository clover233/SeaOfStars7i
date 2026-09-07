import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Douyin_0010(Case):
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

            # 1、点击进入抖音，启动5s，等待2s
            logging.info('点击进入抖音，启动5s，等待2s')
            SeaOfStarsAW.trace_thread.add_log('抖音', '启动抖音，上下切换视频')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(5)

            # 2、浏览推荐视频10s
            time.sleep(10)

            # 3、上下切换视频，切换2s，切换5次
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 4、点击当前视频的up主头像进入主页
            SeaOfStarsAW.ut_device.click(0.927, 0.502)
            time.sleep(2)

            # 5、返回抖音首页
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 6、点击我-关注，点击胡锡进头像查看博主主页信息，等待2s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击关注，查看胡锡进主页')
            SeaOfStarsAW.ut_device(labelContains="我").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="关注").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="胡锡进").click()
            time.sleep(2)

            # 7、上滑5次、下滑5次，等待2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 8、点击播放博主的第一个视频，浏览15s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击播放博主第一个视频，浏览评论')
            SeaOfStarsAW.ut_device.click(0.178, 0.692)
            time.sleep(15)

            # 9、点击视频评论按钮
            SeaOfStarsAW.ut_device.click(0.93, 0.603)
            time.sleep(2)

            # 10、滑动浏览评论，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 11、左滑返回博主主页，1s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 12、点击播放第二个视频，浏览15s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击播放博主第二个视频，浏览评论')
            SeaOfStarsAW.ut_device.click(0.501, 0.687)
            time.sleep(15)

            # 13、点击视频评论按钮
            SeaOfStarsAW.ut_device.click(0.93, 0.603)
            time.sleep(2)

            # 14、滑动浏览评论，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 15、左滑返回博主主页，1s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 16、点击播放第三个视频，浏览15s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击播放博主第三个视频，浏览评论')
            SeaOfStarsAW.ut_device.click(0.833, 0.684)
            time.sleep(15)

            # 17、点击视频评论按钮
            SeaOfStarsAW.ut_device.click(0.93, 0.603)
            time.sleep(2)

            # 18、滑动浏览评论，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 19、左滑返回博主主页，1s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            # 20、左滑两次返回"我的"主页，等待2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            # 21、点击右上方拓展按钮，点击进入观看历史
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击进入观看历史，上下滑动')
            SeaOfStarsAW.ut_device.click(0.924, 0.089)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.383, 0.251)
            time.sleep(1)

            # 22、浏览观看历史，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 23、点击首页，返回推荐页面，2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)

            # 24、返回home页，等待2s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.ugc.Aweme')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')