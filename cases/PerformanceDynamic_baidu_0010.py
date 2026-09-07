import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_baidu_0010(Case):
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

            # 启动百度，停留2S
            # 建议停留3s 跳过3秒广告
            logging.info('1、启动百度')
            SeaOfStarsAW.trace_thread.add_log('百度', '启动百度')
            SeaOfStarsAW.ut_device.session().app_activate('com.baidu.BaiduMobile')
            time.sleep(2)

            # 输入“华为手机”并搜索，停留2S
            # 不建议ai模式搜索
            logging.info('2、输入“华为手机”并搜索')
            SeaOfStarsAW.trace_thread.add_log('百度', '输入“华为手机”并搜索')
            SeaOfStarsAW.ut_device.click(0.172, 0.099, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("华为手机")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.87, 0.099, 0.2)
            SeaOfStarsAW.ut_device.click(0.845, 0.14, 0.2)
            time.sleep(1)

            # 向下滑动6次，停留2S
            logging.info('3、向下滑动6次')
            SeaOfStarsAW.trace_thread.add_log('百度', '向下滑动6次')
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 向上滑动6次至底部，停留2S
            logging.info('4、向上滑动6次')
            SeaOfStarsAW.trace_thread.add_log('百度', '向上滑动6次')
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 侧滑返回首页，停留2S
            logging.info('5、侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log('百度', '侧滑返回首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 返回桌面
            logging.info('6、返回桌面')
            SeaOfStarsAW.trace_thread.add_log('百度', '返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.baidu.BaiduMobile')
            time.sleep(1)

        logging.info('用例执行结束')