import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_taobao_0010(Case):
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
            logging.info('启动淘宝')
            # SeaOfStarsAW.trace_thread.add_log('QQ', '应用启动')
            SeaOfStarsAW.ut_device.app_activate('com.taobao.taobao4iphone')
            logging.info('等待5s')
            time.sleep(5)
            SeaOfStarsAW.ut_device(label="搜索栏").click()
            time.sleep(5)
            SeaOfStarsAW.ut_device.send_keys('清风卫生纸')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('浏览搜索结果，上滑5次，下滑6次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击销量')
            SeaOfStarsAW.ut_device.click(0.196, 0.439)
            time.sleep(2)
            logging.info('点击第一条商品')
            SeaOfStarsAW.ut_device.click(0.236, 0.665)
            time.sleep(2)
            logging.info('浏览商品详情，上滑5次，下滑4次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[2]/Image[16]').click()
            logging.info('点击评论区')
            SeaOfStarsAW.ut_device.click(0.44, 0.483)
            time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击客服')
            SeaOfStarsAW.ut_device.click(0.18, 0.927)
            time.sleep(3)
            logging.info('点击输入框，输入你好')
            SeaOfStarsAW.ut_device.click(0.376, 0.92)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys('你好')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='发送').click()
            time.sleep(2)
            logging.info('点击加号')
            SeaOfStarsAW.ut_device.click(0.926, 0.585)
            logging.info('点击相册')
            SeaOfStarsAW.ut_device.click(0.373, 0.689)
            time.sleep(2)
            logging.info('选择图片')
            SeaOfStarsAW.ut_device.click(0.22, 0.113)
            time.sleep(2)
            logging.info('点击发送')
            # SeaOfStarsAW.ut_device(label='发送（1）').click()
            SeaOfStarsAW.ut_device.click(0.863, 0.933)
            time.sleep(2)
            # SeaOfStarsAW.ut_device.swipe_back()
            # SeaOfStarsAW.ut_device(label='返回').click()
            logging.info('点击返回')
            SeaOfStarsAW.ut_device.xpath('//*[@label="返回，按钮"]').click()
            time.sleep(2)
            logging.info('点击店铺浏览')
            SeaOfStarsAW.ut_device.click(0.066, 0.926)
            time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回')
            # SeaOfStarsAW.ut_device(label='返回').click()
            SeaOfStarsAW.ut_device.click(0.06, 0.075)
            time.sleep(2)
            # SeaOfStarsAW.ut_device.xpath('//*[@label="返回，按钮"]').click()
            # time.sleep(0.5)
            logging.info('点击加入购物车')
            # SeaOfStarsAW.ut_device.click(0.433, 0.93)
            SeaOfStarsAW.ut_device(label='加入购物车').click()
            time.sleep(2)
            logging.info('点击返回商品详情')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')