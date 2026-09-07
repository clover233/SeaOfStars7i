import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Dongchedi_0010(Case):
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

            # 1、打开懂车帝，等待2s
            logging.info('打开懂车帝，等待2s')
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '1、打开懂车帝，点击兴趣圈滑动')
            SeaOfStarsAW.ut_device.click(0.616, 0.364)
            time.sleep(5)

            # 2、点击兴趣圈，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '2、上下滑动各五次 每次停留2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 3、上滑5次，下滑5次，浏览兴趣圈，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '3、点击关注 停留2s')
            SeaOfStarsAW.ut_device(labelContains="关注").click()
            time.sleep(2)

            # 4、点击"话题"帖子，停留2s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '4、上下各滑动2次 每次停留2s')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 5、点击第一条帖子，停留2s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '5、点击 推荐 返回推荐界面  2s')
            SeaOfStarsAW.ut_device(labelContains="推荐").click()
            time.sleep(2)

            # 6、上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '6、点击 搜索框 1s')
            SeaOfStarsAW.ut_device.click(0.498, 0.081)
            time.sleep(1)

            # 7、右下角点赞，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '7、输入 奥迪A8 停留1s 点击搜索 停留1s')
            SeaOfStarsAW.ut_device().set_text("奥迪A8")
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 8、点击评论查看，等待1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '8、点击第一个结果 停留1s')
            SeaOfStarsAW.ut_device.click(0.55, 0.298)
            time.sleep(1)

            # 9、返回首页，等待1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '9、点击图片 停留2s')
            SeaOfStarsAW.ut_device.click(0.492, 0.256)
            time.sleep(2)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '10、点击查看第一张图片 停留2s')
            SeaOfStarsAW.ut_device.click(0.168, 0.579)
            time.sleep(2)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '11、左滑3次 右滑2次  每次停留2s')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '12、返回上一界面')
            SeaOfStarsAW.ut_device.click(0.064, 0.082)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '13、重复5次 上下滑动1次 每次停留1s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '14、返回搜索界面')
            SeaOfStarsAW.ut_device.click(0.064, 0.082)
            SeaOfStarsAW.ut_device.click(0.064, 0.082)
            SeaOfStarsAW.ut_device.click(0.064, 0.082)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '15、点击热榜喜爱 第一条 停留2s')
            SeaOfStarsAW.ut_device.click(0.33, 0.547)
            time.sleep(2)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '16、上下各滑动2次 停留2s')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '17、返回首页 返回homoe')
            SeaOfStarsAW.ut_device.click(0.064, 0.082)
            SeaOfStarsAW.ut_device.click(0.064, 0.082)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)



        logging.info('用例执行结束')