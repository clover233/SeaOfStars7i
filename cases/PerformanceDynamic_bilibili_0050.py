import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_bilibili_0050(Case):
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

            # 1、启动哔哩哔哩
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('tv.danmaku.bilianime')

            # 2、点击底部Tab动态
            logging.info('2、点击底部Tab动态')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击底部Tab动态')
            SeaOfStarsAW.ut_device.click(0.307, 0.927, 0.50)
            time.sleep(1)

            # 3、上滑5次浏览动态页
            logging.info('3、上滑5次浏览动态页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '上滑5次浏览动态页')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 4、下滑5次浏览动态页
            logging.info('4、下滑5次浏览动态页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '下滑5次浏览动态页')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 5、点击屏幕一条视频播放
            logging.info('5、点击屏幕一条视频播放')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击屏幕一条视频播放')
            SeaOfStarsAW.ut_device.click(0.477, 0.535, 0.50)
            time.sleep(1)

            # 6、观看视频10秒
            logging.info('6、观看视频10秒')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '观看视频10秒')
            time.sleep(10)

            # 7、返回首页
            logging.info('7、返回首页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.114, 0.928, 0.50)
            time.sleep(1)

            # 8、上滑返回桌面
            logging.info('8、返回桌面')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('tv.danmaku.bilianime')
            time.sleep(1)

        logging.info('用例执行结束')