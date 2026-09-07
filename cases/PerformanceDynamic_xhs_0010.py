import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xhs_0010(Case):
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

            step1 = "'1、打开小红书,等待10s'"
            logging.info('启动小红书')
            SeaOfStarsAW.trace_thread.add_log('小红书', step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.149, 0.714)
            time.sleep(10)

            step2 = "2、点击我的 -进入收藏 - 图片链接"
            SeaOfStarsAW.trace_thread.add_log('小红书', step2)
            SeaOfStarsAW.ut_device.click(0.904, 0.936)
            SeaOfStarsAW.ut_device(labelContains="收藏").click()
            SeaOfStarsAW.ut_device.click(0.216, 0.68)
            time.sleep(1)

            step3 = "3、左下角点赞"
            SeaOfStarsAW.trace_thread.add_log('小红书', step3)
            SeaOfStarsAW.ut_device(labelContains="点赞").click()
            time.sleep(1)

            step4 = "4、浏览图片，左滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step4)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)

            step5 = "5、返回我的页面 停留1s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step5)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device(labelContains="正文").click()
            time.sleep(5)

            step6 = "6、点击设置图标 停留1s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step6)
            SeaOfStarsAW.ut_device(labelContains="设置").click()
            time.sleep(1)

            step7 = "7、返回首页 停留1s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step7)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.click(0.128, 0.935)
            time.sleep(1)

            step8 = "8、上滑5次 下滑6次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step8)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step9 = "9、点击 消息"
            SeaOfStarsAW.trace_thread.add_log('小红书', step9)
            SeaOfStarsAW.ut_device.click(0.706, 0.945)

            step10 = "10、点击 我"
            SeaOfStarsAW.trace_thread.add_log('小红书', step10)
            SeaOfStarsAW.ut_device.click(0.896, 0.941)
            time.sleep(3)

            step11 = "11、点击 消息"
            SeaOfStarsAW.trace_thread.add_log('小红书', step11)
            SeaOfStarsAW.ut_device.click(0.706, 0.945)

            step12 = "12、点击 首页"
            SeaOfStarsAW.trace_thread.add_log('小红书', step12)
            SeaOfStarsAW.ut_device.click(0.128, 0.935)
            time.sleep(1)

            step13 = "13、点击 + 进入相册 停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step13)
            SeaOfStarsAW.ut_device(labelContains="发布标签").click()
            SeaOfStarsAW.ut_device(labelContains="相册").click()
            time.sleep(2)

            step14 = "14、上滑3次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step14)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step15 = "15、点击第一张图片 大图查看 停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step15)
            SeaOfStarsAW.ut_device.click(0.528, 0.411)
            time.sleep(2)

            step16 = "16、滑动浏览 左滑3次 右滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log('小红书', step16)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            step17 = "17、侧滑2次  返回首页"
            SeaOfStarsAW.trace_thread.add_log('小红书', step17)
            SeaOfStarsAW.ut_device.click(0.068, 0.106)
            SeaOfStarsAW.ut_device.click(0.068, 0.106)

            step18 = "18、返回home页面"
            SeaOfStarsAW.trace_thread.add_log('小红书', step18)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')