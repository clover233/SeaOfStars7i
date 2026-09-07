import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Douyin_0030(Case):
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
            step = 0
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、点击进入抖音，启动5s，等待2s
            logging.info('点击进入抖音，等待3s')
            SeaOfStarsAW.trace_thread.add_log('抖音', '启动抖音，进入聊天界面，发送华为手机')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(5)

            # 2、进入消息页面，1s
            SeaOfStarsAW.ut_device(labelContains="消息").click()
            time.sleep(1)

            # 3、进入测试账号聊天页面，2s
            SeaOfStarsAW.ut_device(labelContains="动态模型xx").click()
            time.sleep(2)

            # 4、发送文字华为手机，2s
            SeaOfStarsAW.ut_device.click(0.287, 0.934)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("华为手机")
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="发送").click()
            time.sleep(2)

            # 5、点击"+"，停留1s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击拍摄，发送图片')
            SeaOfStarsAW.ut_device(labelContains="更多面板").click()
            time.sleep(1)

            # 6、点击拍摄，等待2s
            SeaOfStarsAW.ut_device(labelContains="拍摄").click()
            time.sleep(2)

            # 7、拍摄图片，等待2s
            SeaOfStarsAW.ut_device.click(0.501, 0.82)
            time.sleep(2)

            # 8、点击发送，等待2s
            SeaOfStarsAW.ut_device(labelContains="发送").click()
            time.sleep(2)

            # 9、点击"+"，停留1s
            # SeaOfStarsAW.ut_device.click(0.93, 0.603)
            # time.sleep(2)

            # 10、点击相册，停留1s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击相册，上下滑动，发送图片')
            SeaOfStarsAW.ut_device(labelContains="相册").click()
            time.sleep(1)

            # 11、上滑3次，下滑3次，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 12、点击第一张图片，停留1s
            SeaOfStarsAW.ut_device.click(0.154, 0.586)
            time.sleep(1)

            # 13、点击发送，停留2s
            SeaOfStarsAW.ut_device(labelContains="发送").click()
            time.sleep(2)

            # 14、返回消息页面，停留1s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

            # 15、查看系统消息，2s
            # for i in range(2):
            #     SeaOfStarsAW.ut_device.swipe_right()
            # time.sleep(2)

            # 16、上滑3次，下滑3次，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)


            # 17、点击首页，返回推荐页面，2s
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)

            # 18、返回home页，等待2s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.ugc.Aweme')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')