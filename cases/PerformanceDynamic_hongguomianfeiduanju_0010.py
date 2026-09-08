import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hongguomianfeiduanju_0010(Case):
    all_app_package_list = ['com.phoenix.video']
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
            app_name = '红果免费短剧'

            logging.info('1、启动红果免费短剧')
            SeaOfStarsAW.trace_thread.add_log(app_name, '1、启动红果免费短剧')
            SeaOfStarsAW.ut_device.app_activate('com.phoenix.video')
            time.sleep(3)

            logging.info('2、向上抛滑5次，浏览首页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '2、向上抛滑5次，浏览首页')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('3、向下抛滑5次，浏览首页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '3、向下抛滑5次，浏览首页')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('4、点击剧场按钮，进入剧场页面')
            SeaOfStarsAW.trace_thread.add_log(app_name, '4、点击剧场按钮，进入剧场页面')
            theater_tab = SeaOfStarsAW.ut_device(labelContains='剧场')
            if theater_tab.exists:
                theater_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.3, 0.95)
            time.sleep(2)

            logging.info('5、向上滑动5次，浏览找剧页面')
            SeaOfStarsAW.trace_thread.add_log(app_name, '5、向上滑动5次，浏览找剧页面')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('6、向下滑动5次，浏览找剧页面')
            SeaOfStarsAW.trace_thread.add_log(app_name, '6、向下滑动5次，浏览找剧页面')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('7、点击排行榜，进入红果推荐榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '7、点击排行榜，进入红果推荐榜')
            ranking_button = SeaOfStarsAW.ut_device(labelContains='排行榜')
            if ranking_button.exists:
                ranking_button.click()
            else:
                SeaOfStarsAW.ut_device.click(0.85, 0.18)
            time.sleep(2)

            logging.info('8、向上滑动5次，浏览红果推荐榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '8、向上滑动5次，浏览红果推荐榜')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('9、向下滑动5次，浏览红果推荐榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '9、向下滑动5次，浏览红果推荐榜')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('10、点击推荐榜第一的短剧，观看视频15s')
            SeaOfStarsAW.trace_thread.add_log(
                app_name,
                '10、点击推荐榜第一的短剧，观看视频15s',
            )
            SeaOfStarsAW.ut_device.click(0.5, 0.35)
            time.sleep(15)

            logging.info('11、返回红果推荐榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '11、返回红果推荐榜')
            SeaOfStarsAW.ut_device.swipe(
                0.01,
                0.5,
                0.95,
                0.5,
                duration=0.5,
            )
            time.sleep(2)

            logging.info('12、点击热播榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '12、点击热播榜')
            hot_ranking_tab = SeaOfStarsAW.ut_device(labelContains='热播榜')
            if hot_ranking_tab.exists:
                hot_ranking_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.65, 0.15)
            time.sleep(2)

            logging.info('13、向上滑动5次，浏览热播榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '13、向上滑动5次，浏览热播榜')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('14、向下滑动5次，浏览热播榜')
            SeaOfStarsAW.trace_thread.add_log(app_name, '14、向下滑动5次，浏览热播榜')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            logging.info('15、点击热播榜第一的短剧，观看视频15s')
            SeaOfStarsAW.trace_thread.add_log(
                app_name,
                '15、点击热播榜第一的短剧，观看视频15s',
            )
            SeaOfStarsAW.ut_device.click(0.5, 0.35)
            time.sleep(15)

            logging.info('16、返回剧场界面')
            SeaOfStarsAW.trace_thread.add_log(app_name, '16、返回剧场界面')
            # 第一次返回热播榜，第二次退出排行榜并回到剧场。
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe(
                    0.01,
                    0.5,
                    0.95,
                    0.5,
                    duration=0.5,
                )
                time.sleep(2)

            logging.info('17、点击我的，进入我的界面')
            SeaOfStarsAW.trace_thread.add_log(app_name, '17、点击我的，进入我的界面')
            mine_tab = SeaOfStarsAW.ut_device(label='我的')
            if mine_tab.exists:
                mine_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.9, 0.95)
            time.sleep(2)

            logging.info('18、上滑一次，浏览观看历史')
            SeaOfStarsAW.trace_thread.add_log(app_name, '18、上滑一次，浏览观看历史')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            logging.info('19、下滑一次，浏览观看历史')
            SeaOfStarsAW.trace_thread.add_log(app_name, '19、下滑一次，浏览观看历史')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            logging.info('20、点击首页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '20、点击首页')
            home_tab = SeaOfStarsAW.ut_device(label='首页')
            if home_tab.exists:
                home_tab.click()
            else:
                SeaOfStarsAW.ut_device.click(0.1, 0.95)
            time.sleep(2)

            logging.info('21、滑动返回Home页')
            SeaOfStarsAW.trace_thread.add_log(app_name, '21、滑动返回Home页')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            time.sleep(1)

            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
