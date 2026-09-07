import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0110(Case):
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
            SeaOfStarsAW.trace_thread.add_log('微信', '打开服务')
            logging.info('点击我')
            SeaOfStarsAW.ut_device(label='我').click()
            time.sleep(2)
            logging.info('点击服务')
            SeaOfStarsAW.ut_device(label='服务').click()
            time.sleep(2)
            logging.info('上滑')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            SeaOfStarsAW.trace_thread.add_log('微信', '打开拼多多')
            logging.info('点击拼多多')
            SeaOfStarsAW.ut_device(label='拼多多').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '拼多多内容浏览')
            logging.info('上滑6次，下滑6次')
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            logging.info('点击电影演出玩乐')   # 有广告
            SeaOfStarsAW.trace_thread.add_log('微信', '打开电影演出玩乐')
            SeaOfStarsAW.ut_device(label='电影演出玩乐').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '电影演出玩乐内容浏览')
            logging.info('上滑6次，下滑6次')
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击电影/影院')
            SeaOfStarsAW.ut_device.click(0.116, 0.294)
            time.sleep(2)
            logging.info('上滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            logging.info('点击品牌发现')
            SeaOfStarsAW.trace_thread.add_log('微信', '打开品牌发现')
            SeaOfStarsAW.ut_device(label='品牌发现').click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '品牌发现浏览')
            logging.info('上滑6次，下滑6次')
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '返回发现页')
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击收藏')
            SeaOfStarsAW.trace_thread.add_log('微信', '打开收藏')
            SeaOfStarsAW.ut_device(label='收藏').click()
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.126, 0.95)
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('微信', '返回桌面')
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')