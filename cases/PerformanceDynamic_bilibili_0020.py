import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_bilibili_0020(Case):
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

            # 1、启动哔哩哔哩(1s，停留1s)
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('tv.danmaku.bilianime')

            # 2、首页——推荐(1s，停留3s)
            logging.info('2、首页——推荐')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '首页——推荐')
            SeaOfStarsAW.ut_device.click(0.264, 0.142, 0.2)
            time.sleep(3)

            # 3、浏览（上下滑动5次, 每次停留2s）
            logging.info('3、上下滑动5次')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '上下滑动5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、进入热门(1s，停留1s)
            logging.info('4、进入热门')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '进入热门')
            SeaOfStarsAW.ut_device.click(0.408, 0.143, 0.5)
            time.sleep(1)

            # 5、点击的第一个视频播放（1s，停留20s）
            logging.info('5、点击的第一个视频播放')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击的第一个视频播放')
            SeaOfStarsAW.ut_device.click(0.465, 0.33, 0.5)
            time.sleep(20)

            # 6、点击视频的up主（1s，停留1s）
            logging.info('6、点击视频的up主')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击视频的up主')
            SeaOfStarsAW.ut_device.click(0.469, 0.476, 0.3)
            SeaOfStarsAW.ut_device.click(0.474, 0.406, 0.5)
            time.sleep(3)

            # 7、浏览up主（上下滑动5次, 每次停留2s）
            logging.info('7、上下滑动5次')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '上下滑动5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 8、点击up主第一个视频播放
            logging.info('8、点击up主第一个视频播放')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击up主第一个视频播放')
            SeaOfStarsAW.ut_device.click(0.537, 0.68, 0.5)
            time.sleep(3)

            # 9、点击视频下的评论
            logging.info('9、点击视频下的评论')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击视频下的评论')
            SeaOfStarsAW.ut_device.click(0.344, 0.351, 0.5)
            time.sleep(3)

            # 10、滑动评论（上下滑动5次, 每次停留2s）
            logging.info('10、滑动评论')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '滑动评论')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 11、返回哔哩哔哩首页(需3次返回，停留1s)
            logging.info('11、返回哔哩哔哩首页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回哔哩哔哩首页')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.994, 0.585, 1.0)
                time.sleep(1)

            # 12、返回home页面(1s，停留1s)
            logging.info('12、返回桌面')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('tv.danmaku.bilianime')
            time.sleep(1)

        logging.info('用例执行结束')