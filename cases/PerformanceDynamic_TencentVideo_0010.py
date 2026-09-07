import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_TencentVideo_0010(Case):
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


            logging.info('启动腾讯视频')
            # SeaOfStarsAW.trace_thread.add_log('微信', '启动微信')
            SeaOfStarsAW.ut_device.click(0.84, 0.474)
            logging.info('等待8s')
            time.sleep(8)
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '主页浏览，上滑5次，下滑2次')
            logging.info('上滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '浏览电视剧')
            logging.info('点击电视剧')
            SeaOfStarsAW.ut_device(label='电视剧').click()
            time.sleep(2)
            logging.info('点击主页第一个推荐视频')   # 注意有广告情况
            # SeaOfStarsAW.trace_thread.add_log('微信', '启动微信')
            SeaOfStarsAW.ut_device.click(0.513, 0.268)
            time.sleep(30)
            logging.info('点击屏幕现实横屏标志')
            SeaOfStarsAW.ut_device.click(0.936, 0.281)
            time.sleep(1)
            logging.info('切换到全屏')
            SeaOfStarsAW.ut_device.click(0.936, 0.281)
            time.sleep(10)
            logging.info('点击屏幕现实横屏标志')
            SeaOfStarsAW.ut_device.click(0.936, 0.281)
            time.sleep(1)
            logging.info('退出全屏')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '浏览电视集数)
            logging.info('浏览为你推荐，上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '浏览视频播放界面)
            logging.info('点击搜索栏')
            SeaOfStarsAW.ut_device.click(0.503, 0.072)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('斗破苍穹')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('浏览为你推荐，上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击影视')
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '浏览影视界面)
            SeaOfStarsAW.ut_device.click(0.196, 0.115)
            time.sleep(2)
            logging.info('浏览为你推荐，上滑1次，下滑1次')
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('腾讯视频', '浏返回首页+退出app)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            logging.info('上滑退出腾讯视频')
            # SeaOfStarsAW.trace_thread.add_log('微信', '上滑退出微信')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')