import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Weibo_0030(Case):
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

            # 1、启动微博
            logging.info('启动微博')
            SeaOfStarsAW.trace_thread.add_log('微博', '1、打开微博,等待3s')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.6)
            time.sleep(10)

            # 2、点击发现，等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '2、点击发现，等待1s')
            SeaOfStarsAW.ut_device.click(0.507, 0.942)
            time.sleep(1)

            # 3、点击更多热搜， 进入热搜界面
            SeaOfStarsAW.trace_thread.add_log('微博', '3、点击更多热搜， 进入热搜界面')
            SeaOfStarsAW.ut_device(labelContains="更多热搜").click()
            time.sleep(2)
            # 4、上滑5次，下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '4、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、点击 热搜第一条 等待3s
            SeaOfStarsAW.trace_thread.add_log('微博', '5、点击 热搜第一条 等待3s')
            SeaOfStarsAW.ut_device.click(0.412, 0.3)
            time.sleep(3)
            # 6、点击视频 第一条博文 查看正文 等待3s
            SeaOfStarsAW.trace_thread.add_log('微博', '6、点击视频 第一条博文 查看正文 等待3s')
            SeaOfStarsAW.ut_device(labelContains="视频").click()
            SeaOfStarsAW.ut_device(labelContains="正文").click()
            time.sleep(3)

            # 7、上滑5次、下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '7、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 8、点击右下角 赞 等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '8、点击右下角 赞 等待1s')
            SeaOfStarsAW.ut_device.swipe_down()
            SeaOfStarsAW.ut_device(labelContains="赞").click()
            time.sleep(1)
            # 9、点击右下角 赞 等待1s 从而取消赞
            SeaOfStarsAW.trace_thread.add_log('微博', '9、点击右下角赞 取消赞')
            SeaOfStarsAW.ut_device(labelContains="赞").click()
            time.sleep(1)
            # 10、点击评论 输入评论 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '10、点击评论 输入评论 等待2s')
            SeaOfStarsAW.ut_device(labelContains="评论").click()
            SeaOfStarsAW.ut_device().set_text("评论")
            time.sleep(2)

            # 11、点击取消 到达博文正文界面
            SeaOfStarsAW.trace_thread.add_log('微博', '11、点击取消 到达博文正文界面')
            SeaOfStarsAW.ut_device.click(0.412, 0.3)

            # 12、点击转发微博 等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '12、点击第一条博文的第一张图片 查看大图，等待1s')
            SeaOfStarsAW.ut_device(labelContains="转发").click()
            time.sleep(1)

            # 13、点击取消
            SeaOfStarsAW.trace_thread.add_log('微博', '13、点击取消')
            SeaOfStarsAW.ut_device(labelContains="取消").click()
            # 14、点击返回，返回页面
            SeaOfStarsAW.trace_thread.add_log('微博', '14、左滑3次，返回页面')
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.044, 0.086)
            SeaOfStarsAW.ut_device(labelContains="微博").click()

            # 15、上滑返回到home 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '15、上滑返回到home 等待2s')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_right()


        logging.info('用例执行结束')