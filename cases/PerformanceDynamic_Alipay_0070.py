import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Alipay_0070(Case):
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

            # 1、启动支付宝（停留2s) 建议关掉推送悬浮窗、医疗健康在更多服务第一个；蚂蚁森林在更多服务第二个
            logging.info('1、应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.alipay.iphoneclient')
            time.sleep(2)

            # 2、点击“医疗健康”（停留2s)
            logging.info('2、点击“医疗健康”')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击“医疗健康”')
            SeaOfStarsAW.ut_device.click(0.112, 0.26, 0.20)
            time.sleep(2)

            # 3、侧滑返回首页（停留2s)
            logging.info('3、侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '侧滑返回首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 4、第二次点击“医疗健康”（停留2s)
            logging.info('4、第二次点击“医疗健康”')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '第二次点击“医疗健康”')
            SeaOfStarsAW.ut_device.click(0.112, 0.26, 0.20)
            time.sleep(2)

            # 5、上滑1次浏览（停留2s)
            logging.info('5、上滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 6、下滑1次浏览（停留2s)
            logging.info('6、下滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 7、侧滑返回首页（停留2s)
            logging.info('7、侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '侧滑返回首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 8、点击“蚂蚁森林”（停留2s)
            logging.info('8、点击“蚂蚁森林”')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击“蚂蚁森林”')
            SeaOfStarsAW.ut_device.click(0.304, 0.261, 0.20)
            time.sleep(2)

            # 9、上滑1次浏览（停留2s)
            logging.info('9、上滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 10、下滑1次浏览（停留2s)
            logging.info('10、下滑1次浏览')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑1次浏览')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 11、点击“返回”按钮，返回首页（停留2s)
            logging.info('返11、回首页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回首页')
            SeaOfStarsAW.ut_device.click(0.066, 0.088, 0.20)
            time.sleep(2)

            # 12、点击视频（停留2s)
            logging.info('12、点击视频')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击视频')
            SeaOfStarsAW.ut_device.click(0.494, 0.918, 0.20)
            time.sleep(2)

            # 13、上滑5次，下滑5次观看视频（停留2s)
            logging.info('13、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('13、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 14、点击评论（停留2s)
            logging.info('14、点击评论')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击评论')
            SeaOfStarsAW.ut_device.click(0.925, 0.661, 0.20)
            time.sleep(2)

            # 15、退出评论（停留2s)
            logging.info('15、退出评论')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '退出评论')
            SeaOfStarsAW.ut_device.click(0.477, 0.155, 0.20)
            time.sleep(2)

            # 16、点击直播（停留2s)
            logging.info('16、点击直播')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击直播')
            SeaOfStarsAW.ut_device.click(0.497, 0.081, 0.20)
            time.sleep(2)

            # 17、上滑5次，下滑5次观看视频（停留1s)
            logging.info('17、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            logging.info('17、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)
            time.sleep(1)

            # 18、进入直播间观看直播10s
            logging.info('18、进入直播间观看直播')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '进入直播间观看直播')
            SeaOfStarsAW.ut_device.click(0.497, 0.721, 0.10)
            time.sleep(5)
            time.sleep(5)

            # 19、退出直播间（停留2s)
            logging.info('19、退出直播间')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '退出直播间')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.2)
            time.sleep(2)

            # 20、点击短剧（停留2s)
            logging.info('20、点击短剧')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击短剧')
            SeaOfStarsAW.ut_device.click(0.62, 0.08, 0.20)
            time.sleep(2)

            # 21、上滑5次，下滑5次浏览短剧页面（停留2s)
            logging.info('21、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('21、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 22、点击热播榜（停留2s) 有的视频不会显示热播榜 建议从搜索固定进入
            logging.info('22、点击热播榜')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击热播榜')
            SeaOfStarsAW.ut_device.click(0.893, 0.079, 0.20)
            time.sleep(2)

            # 23、上滑2次，下滑2次浏览热播榜（停留2s)
            logging.info('23、上滑2次，下滑2次浏览热播榜')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑2次，下滑2次浏览热播榜')
            logging.info('上滑2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('下滑2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 24、点击播放热播榜第一的短剧观看15s
            logging.info('24、点击播放热播榜第一的短剧观看15s')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击播放热播榜第一的短剧观看15s')
            SeaOfStarsAW.ut_device.click(0.252, 0.512, 0.25)
            time.sleep(5)
            time.sleep(5)
            time.sleep(5)

            # 25、返回视频页（停留2s)
            logging.info('25、返回视频页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回视频页')
            SeaOfStarsAW.ut_device.click(0.051, 0.089, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.051, 0.089, 0.2)
            time.sleep(2)

            # 26、返回首页（停留2s)
            logging.info('26、返回首页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回首页')
            SeaOfStarsAW.ut_device.click(0.094, 0.928, 0.2)
            time.sleep(2)

            # 27、返回home页
            logging.info('27、返回home页面(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回home页面(停留1s)')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.alipay.iphoneclient')

        logging.info('用例执行结束')