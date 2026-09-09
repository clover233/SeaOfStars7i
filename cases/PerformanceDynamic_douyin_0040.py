import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_douyin_0040(Case):
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
            SeaOfStarsAW.trace_thread.add_log('抖音', '启动抖音，上下滑动10次')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(3)

            # 2、上滑10次浏览页推荐视频
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 3、下滑10次浏览页推荐视频
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 4、搜索胡锡进
            SeaOfStarsAW.trace_thread.add_log('抖音', '搜索胡锡进')
            SeaOfStarsAW.ut_device.click(0.936, 0.086)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys("胡锡进")
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 5、返回首页
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)


            # 6、点击评论按钮
            SeaOfStarsAW.trace_thread.add_log('抖音', '返回首页，点击评论，输入评论并发送')
            SeaOfStarsAW.ut_device.click(0.931, 0.629)
            time.sleep(1)

            # 7、点击输入框
            SeaOfStarsAW.ut_device.click(0.287, 0.938)
            time.sleep(2)

            # 8、输入"我是评论ABC"
            SeaOfStarsAW.ut_device().set_text("我是评论ABC")
            time.sleep(2)

            # 9、点击发送
            SeaOfStarsAW.ut_device(labelContains="发送").click()
            time.sleep(2)

            # 10、侧滑一次返回
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

            # 11、点击点赞按钮
            SeaOfStarsAW.ut_device.click(0.928, 0.555)
            time.sleep(2)

            # 12、点击商城，2s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击商城，搜索商品，浏览，点击客服，点击店铺')
            SeaOfStarsAW.ut_device(labelContains="我").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.102, 0.413)
            time.sleep(1)

            # 13、上滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 14、下滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 15、搜索华为P70，2s
            SeaOfStarsAW.ut_device.click(0.356, 0.093)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("华为P70")
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 16、上滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 17、下滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 18、点击第一个商品，2s
            SeaOfStarsAW.ut_device.click(0.178, 0.326)
            time.sleep(2)

            # 19、上滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 20、点击左下角客服，2s
            SeaOfStarsAW.ut_device.click(0.191, 0.924)
            time.sleep(2)

            # 21、返回到商品详情页，2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 22、点击左下角进入店铺，2s
            SeaOfStarsAW.ut_device.click(0.075, 0.924)
            time.sleep(2)

            # 23、上滑三次浏览推荐商品，2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 24、点击首页，返回推荐页面，2s
            SeaOfStarsAW.trace_thread.add_log('抖音', '返回首页，点击精选-团购-关注-推荐')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)

            # 25、点击长视频，2s
            SeaOfStarsAW.ut_device(labelContains="精选").click()
            time.sleep(2)

            # 26、向左滑动，依次切换顶部tab页（长视频-关注-商城-推荐），循环3次
            for i in range(3):
                SeaOfStarsAW.ut_device(labelContains="团购").click()
                SeaOfStarsAW.ut_device(labelContains="关注").click()
                SeaOfStarsAW.ut_device(labelContains="推荐").click()
                time.sleep(2)
            # 27、返回home页，等待2s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.ugc.Aweme')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')