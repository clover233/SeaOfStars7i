import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_AutoNavi_0060(Case):
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

            # 1、启动高德地图，停留3s
            logging.info('1、启动高德地图')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '启动高德地图')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(3)

            # 2、点击搜索框，停留2s
            logging.info('2、点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击搜索框')
            SeaOfStarsAW.ut_device.click(0.922, 0.475, 0.2)
            time.sleep(2)


            # 3、输入“西安北站”并搜索，停留2s
            logging.info('3、输入“西安北站”并搜索')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '输入“西安北站”并搜索')
            SeaOfStarsAW.ut_device.click(0.298, 0.138, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("西安北站")
            time.sleep(1)

            # 4、点击第一个搜索结果的路线 ，停留2s
            logging.info('4、点击第一个搜索结果的路线')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击第一个搜索结果的路线')
            SeaOfStarsAW.ut_device.click(0.512, 0.256, 0.2)
            time.sleep(2)

            # 5、点击开始导航，停留2s
            logging.info('5、点击开始导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击开始导航')
            SeaOfStarsAW.ut_device.click(0.699, 0.942, 0.2)
            time.sleep(2)

            # 6、上滑，将高德地图放入后台，停留2s
            logging.info('6、上滑')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

            # 7、启动小红书，停留2s
            logging.info('7、启动小红书')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '启动小红书')
            SeaOfStarsAW.ut_device.session().app_activate('com.xingin.discover')
            time.sleep(3)

            # 8、浏览首页，上滑5次停留，下滑5次，每次停留2s
            logging.info('8、向上滑5次')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('8、向下滑5次')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 9、点击消息，停留2s
            logging.info('9、点击消息')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击消息')
            SeaOfStarsAW.ut_device.click(0.696, 0.934, 0.2)
            time.sleep(2)

            # 10、点击我，停留2s
            logging.info('10、点击我')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击我')
            SeaOfStarsAW.ut_device.click(0.896, 0.935, 0.2)
            time.sleep(2)

            # 11、点击收藏，停留2s
            logging.info('11、点击收藏')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击收藏')
            SeaOfStarsAW.ut_device.click(0.249, 0.488, 0.2)
            time.sleep(2)

            # 12、浏览收藏页，上滑2次，下滑2次，每次停留2s
            logging.info('12、浏览收藏页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '浏览收藏页')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('高德地图', '向下滑5次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 13、返回首页，停留2s
            logging.info('13、返回首页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回首页')
            SeaOfStarsAW.ut_device.click(0.097, 0.934, 0.2)
            time.sleep(2)

            # 14、上滑退出小红书，停留2s
            logging.info('14、上滑退出小红书')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑退出小红书')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

            # 15、打开高德，停留10s
            logging.info('15、打开高德')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '打开高德')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(3)

            # 16、上滑，将高德地图放入后台，停留2s
            logging.info('16、上滑，将高德地图放入后台')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑，将高德地图放入后台')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

            # 17、打开抖音，停留3s com.ss.iphone.ugc.Aweme
            logging.info('17、打开抖音')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '打开抖音')
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(3)

            # 18、首页观看10s
            logging.info('18、首页观看10s')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '首页观看10s')
            time.sleep(10)

            # 19、浏览首页，上滑5次，下滑5次，每次停留2s
            logging.info('19、浏览首页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '浏览首页')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 20、点击顶部热点，停留2s
            logging.info('20、点击顶部热点')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击顶部热点')
            SeaOfStarsAW.ut_device.click(0.223, 0.097, 0.2)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.263, 0.096, 0.2)
            time.sleep(2)

            # 21、浏览热点页面，上滑5次，下滑5次，每次停留2s
            logging.info('21、浏览热点页面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '浏览热点页面')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 22、点击推荐，停留2s
            logging.info('22、点击推荐')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击推荐')
            SeaOfStarsAW.ut_device.click(0.833, 0.096, 0.2)
            time.sleep(2)

            # 23、返回桌面，停留2s
            logging.info('23、返回桌面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回桌面')
            SeaOfStarsAW.ut_device.home()

            # 打开高德，停留2s
            logging.info('打开高德')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '打开高德')
            SeaOfStarsAW.ut_device.session().app_activate('com.autonavi.amap')
            time.sleep(2)

            # 返回首页
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回首页')
            time.sleep(2)

            # 上滑返回桌面
            logging.info('上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.autonavi.amap')

        logging.info('用例执行结束')