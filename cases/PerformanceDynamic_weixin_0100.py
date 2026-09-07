import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0100(Case):
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
            # step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            logging.info('启动微信')
            SeaOfStarsAW.trace_thread.add_log('微信', '微信启动')
            SeaOfStarsAW.ut_device.click(0.606, 0.585)
            logging.info('等待5s')
            time.sleep(5)
            SeaOfStarsAW.trace_thread.add_log('微信', '打开视频号')
            logging.info('点击发现')
            SeaOfStarsAW.ut_device(label='发现').click()
            time.sleep(2)
            logging.info('点击视频号')
            SeaOfStarsAW.ut_device(label='视频号').click()
            time.sleep(2)
            logging.info('上滑6次')
            SeaOfStarsAW.trace_thread.add_log('微信', '浏览视频号')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(4)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device.click(0.043, 0.075)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '打开直播')
            logging.info('点击直播')
            SeaOfStarsAW.ut_device(label='直播').click()
            time.sleep(2)
            logging.info('点击第一个直播')
            SeaOfStarsAW.ut_device.click(0.24, 0.324)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '切换浏览直播')
            logging.info('上滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(4)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.936, 0.081)
            time.sleep(2)
            logging.info('返回主页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击购物')
            SeaOfStarsAW.trace_thread.add_log('微信', '打开购物')
            SeaOfStarsAW.ut_device(label='购物').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '购物界面浏览')
            logging.info('上滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击逛')
            SeaOfStarsAW.trace_thread.add_log('微信', '打开逛')
            SeaOfStarsAW.ut_device.click(0.3, 0.95)
            time.sleep(2)
            logging.info('上滑6次')
            SeaOfStarsAW.trace_thread.add_log('微信', '逛内容浏览')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '打开游戏')
            logging.info('点击游戏')
            SeaOfStarsAW.ut_device(label='游戏').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '游戏内容浏览')
            logging.info('上滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑6次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回桌面')
            SeaOfStarsAW.ut_device.click(0.043, 0.072)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.126, 0.95)
            time.sleep(2)
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')