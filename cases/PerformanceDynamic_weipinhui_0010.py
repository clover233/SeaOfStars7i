import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weipinhui_0010(Case):
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
        # if SeaOfStarsAW.ut_device.locked():
        #     SeaOfStarsAW.ut_device.unlock()
        #     time.sleep(2)

        for test_time in range(0, self.TEST_TIME):
            step = 0
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)
            app_name ="唯品会"

            step1 = "'1、打开唯品会,等待10s'"
            logging.info('启动唯品会')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.367, 0.593)
            time.sleep(10)

            step2 = "2、点击搜索框 输入清风卫生纸  并搜索"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device.click(0.443, 0.077)
            SeaOfStarsAW.ut_device().set_text("清风卫生纸")
            SeaOfStarsAW.ut_device.click(0.889, 0.096)

            step3 = "3、浏览搜索结果 上滑2次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step4 = "4、点击第一条商品 查看详情"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device.click(0.353, 0.256)

            step5 = "5、浏览商品详情 上滑2次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step6 = "6、进入店铺浏览 - 点击店铺图标3s 上滑3cm 停留2s 上滑2次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="进入店铺").click()
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step7 = "7、返回商品详情 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="返回按钮").click()
            time.sleep(2)

            step8 = "8、点后右下角 特卖价 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="购买按钮").click()
            SeaOfStarsAW.ut_device(label="购买按钮").click()
            time.sleep(2)

            step9 = "9、点击 去购物车 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            # SeaOfStarsAW.ut_device(label="去购物车").click()
            SeaOfStarsAW.ut_device(label="购物车按钮").click()
            time.sleep(2)

            step10 = "10、点击结算 2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device(label="结算").click()
            time.sleep(2)

            step11 = "11、返回购物车界面 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device(label="关闭").click()
            SeaOfStarsAW.ut_device(label="返回按钮").click()
            SeaOfStarsAW.ut_device.click(0.364, 0.592)
            time.sleep(2)

            step12 = "12、长按商品 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.swipe(0.778,0.315,0.578,0.315)
            time.sleep(1)

            step13 = "13、点击 删除 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.click(0.876, 0.342)
            time.sleep(1)

            step14 = "14、返回首页 返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device.swipe(0.025, 0.5, 0.925, 0.5)
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.08, 0.09)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')