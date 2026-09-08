import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fanqiechangting_0010(Case):
    all_app_package_list = ['com.xs.fm']
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
        # 清空后台

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

            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'step_' + str(step),
                self.screenshot_dir_path,
            )
            app_name = "番茄畅听"
            
            logging.info('1、启动番茄畅听')
            SeaOfStarsAW.trace_thread.add_log('番茄畅听', '启动番茄畅听')
            SeaOfStarsAW.ut_device.app_activate('com.xs.fm')
            time.sleep(2)

            logging.info('2、首页上滑5次、下滑5次')
            SeaOfStarsAW.trace_thread.add_log(app_name, '2、首页上滑5次、下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('3、搜索“奥运会”')
            SeaOfStarsAW.trace_thread.add_log(app_name, '3、点击搜索框，输入奥运会并搜索')
            search_box = SeaOfStarsAW.ut_device(labelContains='搜索')
            if search_box.exists:
                search_box.click()
            else:
                SeaOfStarsAW.ut_device.click(0.5, 0.08)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text('奥运会')
            time.sleep(1)
            search_button = SeaOfStarsAW.ut_device(label='搜索')
            if search_button.exists:
                search_button.click()
            else:
                SeaOfStarsAW.ut_device.click(0.9, 0.08)
            time.sleep(2)

            logging.info('4、搜索界面上滑5次')
            SeaOfStarsAW.trace_thread.add_log(app_name, '4、搜索界面上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('5、侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '5、侧滑返回首页')
            SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
            time.sleep(2)

            logging.info('6、点击底部短剧')
            SeaOfStarsAW.trace_thread.add_log(app_name, '6、点击底部短剧，进入短剧推荐页面')
            short_drama_tab = SeaOfStarsAW.ut_device(labelContains='短剧')
            if short_drama_tab.exists:
                short_drama_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.5, 0.95)
            time.sleep(2)

            logging.info('7、短剧推荐页面上滑10次')
            SeaOfStarsAW.trace_thread.add_log(app_name, '7、短剧推荐页面上滑10次')
            for _ in range(10):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('8、点击底部首页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '8、点击底部首页')
            home_tab = SeaOfStarsAW.ut_device(label='首页')
            if home_tab.exists:
                home_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.1, 0.95)
            time.sleep(2)

            logging.info('9、首页上滑3次、下滑3次')
            SeaOfStarsAW.trace_thread.add_log(app_name, '9、首页上滑3次、下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('10、点击底部音乐')
            SeaOfStarsAW.trace_thread.add_log(app_name, '10、点击底部音乐')
            music_tab = SeaOfStarsAW.ut_device(labelContains='音乐')
            if music_tab.exists:
                music_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.7, 0.95)
            time.sleep(2)

            logging.info('11、滑动返回Home页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '11、滑动返回Home页')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            time.sleep(1)

            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
