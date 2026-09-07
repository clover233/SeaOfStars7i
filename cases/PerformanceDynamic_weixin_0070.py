import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0070(Case):
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
            # SeaOfStarsAW.trace_thread.add_log('微信', '启动微信')
            SeaOfStarsAW.ut_device.click(0.606, 0.585)
            logging.info('等待5s')
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('微信', '进入瑞幸咖啡小程序')
            logging.info('主页下拉进入小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击瑞幸咖啡小程序')
            SeaOfStarsAW.ut_device(label='瑞幸咖啡').click()
            # SeaOfStarsAW.ut_device.click(0.19, 0.069)
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '点击商品')
            logging.info('点击菜单')
            SeaOfStarsAW.ut_device.click(0.3, 0.943)
            time.sleep(2)
            logging.info('点击店面地址')
            SeaOfStarsAW.ut_device.click(0.246, 0.682)
            time.sleep(2)
            logging.info('点击人气top')
            SeaOfStarsAW.ut_device.click(0.09, 0.205)
            time.sleep(2)
            logging.info('点击第一个商品')
            SeaOfStarsAW.ut_device.click(0.343, 0.307)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑2次，下滑2次')
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)

            logging.info('主页下拉进入小程序')
            # SeaOfStarsAW.trace_thread.add_log('微信', '进入喜茶小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击喜茶小程序')
            SeaOfStarsAW.ut_device(label='喜茶GO').click()
            time.sleep(5)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '点击商品')
            logging.info('点击到店取')
            SeaOfStarsAW.ut_device(label='到店取').click()
            time.sleep(2)
            logging.info('点击第一个商品')
            SeaOfStarsAW.ut_device.click(0.36, 0.611)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑3次，下滑3次')
            logging.info('上滑3次，下滑4次至顶部')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回微信首页')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)


            logging.info('主页下拉进入小程序')
            # SeaOfStarsAW.trace_thread.add_log('微信', '进入美团小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击美团小程序')
            SeaOfStarsAW.ut_device(label='美团丨外卖团购特价美食酒店电影').click()
            time.sleep(5)
            logging.info('上滑3次，下滑3次')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '返回微信首页')
            logging.info('点击返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)

            logging.info('主页下拉进入小程序')
            # SeaOfStarsAW.trace_thread.add_log('微信', '进入蜜雪冰城小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击蜜雪冰城小程序')   # 门店地址需预置
            SeaOfStarsAW.ut_device(label='蜜雪冰城').click()
            time.sleep(5)
            logging.info('点击点餐')
            SeaOfStarsAW.ut_device.click(0.366, 0.927)
            time.sleep(2)
            logging.info('点击选择门店地址')
            SeaOfStarsAW.ut_device.click(0.366, 0.927)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑3次，下滑3次')
            logging.info('上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回微信首页')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)

            logging.info('主页下拉进入小程序')
            # SeaOfStarsAW.trace_thread.add_log('微信', '进入京东购物小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击京东购物小程序')   # 首次有广告，需预置30天内不再出现弹窗
            SeaOfStarsAW.ut_device(label='京东购物丨点外卖领国补').click()
            time.sleep(5)
            logging.info('上滑3次，下滑3次')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回微信首页')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)

            logging.info('主页下拉进入小程序')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击同程旅行小程序')   # 概率性主页白屏
            SeaOfStarsAW.ut_device(label='同程旅行').click()
            time.sleep(5)
            logging.info('点击火车票查询')
            SeaOfStarsAW.ut_device.click(0.486, 0.697)
            time.sleep(2)
            logging.info('上滑3次，下滑3次')
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '商品详情浏览，上滑3次，下滑3次')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击更多日期')
            SeaOfStarsAW.ut_device.click(0.906, 0.127)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微信小程序', '返回微信首页')
            logging.info('点击返回上一页')
            SeaOfStarsAW.ut_device.click(0.046, 0.075)
            time.sleep(2)
            logging.info('点击返回微信首页')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            # SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)
            logging.info('上滑退出微信')
            # SeaOfStarsAW.trace_thread.add_log('微信', '上滑退出微信')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')