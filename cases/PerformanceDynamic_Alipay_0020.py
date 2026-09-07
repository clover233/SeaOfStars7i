import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Alipay_0020(Case):
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

            # 应用启动
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.alipay.iphoneclient')
            time.sleep(2)
            time.sleep(1)

            logging.info('2、切换理财')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '切换理财')
            SeaOfStarsAW.ut_device.click(0.298, 0.923, 0.10)
            time.sleep(1)

            logging.info('3、向上2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向上2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('4、向下2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向下2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            logging.info('5、稳健理财')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '稳健理财')
            SeaOfStarsAW.ut_device.click(0.298, 0.302, 0.10)
            time.sleep(1)

            logging.info('6、向上2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向上2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('7、向下2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向下2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            logging.info('8、点击稳健理财热销第一个理财产品')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击稳健理财热销第一个理财产品')
            SeaOfStarsAW.ut_device.click(0.229, 0.739, 0.10)
            time.sleep(2) # 后面加载快可以注释掉为1

            logging.info('9、向上2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向上2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('10、向下2次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '向下2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            logging.info('11、返回理财页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回理财页')
            for i in range(2):
                SeaOfStarsAW.ut_device.click(0.054, 0.087, 0.10)
                time.sleep(1)
            time.sleep(2)

            logging.info('12、切换消息')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '切换消息')
            SeaOfStarsAW.ut_device.click(0.692, 0.919, 0.10)
            time.sleep(2)

            logging.info('13、点击测试账号进入聊天对话框')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击测试账号进入聊天对话框')
            SeaOfStarsAW.ut_device.click(0.494, 0.401, 0.10)    # 测试账号排布随机，需要调整位置
            time.sleep(2)

            logging.info('14、上滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('15、下滑5次')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            logging.info('16、点击输入框输入动态性能测试')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击输入框输入动态性能测试')
            SeaOfStarsAW.ut_device.click(0.353, 0.857, 0.50)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("动态性能测试")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.879, 0.887, 0.20)
            time.sleep(2)

            logging.info('17、点击图片')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击图片')
            SeaOfStarsAW.ut_device.click(0.939, 0.57, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.16, 0.752, 0.20)
            time.sleep(1)

            logging.info('18、选择5张图片，点击完成')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '选择5张图片，点击完成')
            SeaOfStarsAW.ut_device.click(0.215, 0.355, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.212, 0.47, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.212, 0.583, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.212, 0.701, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.212, 0.813, 0.20)
            time.sleep(1)

            SeaOfStarsAW.ut_device.click(0.925, 0.932, 0.20)
            time.sleep(1)


            logging.info('19、返回消息页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回消息页')
            SeaOfStarsAW.ut_device.click(0.054, 0.084, 0.20)
            time.sleep(1)

            logging.info('20、点击右上角“+”号')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击右上角“+”号')
            SeaOfStarsAW.ut_device.click(0.936, 0.088, 0.20)
            time.sleep(1)

            logging.info('21、点击扫一扫（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击扫一扫（停留2s)')
            SeaOfStarsAW.ut_device.click(0.833, 0.27, 0.20)
            time.sleep(2)

            logging.info('22、点击相册（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击相册（停留2s)')
            SeaOfStarsAW.ut_device.click(0.876, 0.808, 0.20)
            time.sleep(2)

            logging.info('23、返回消息页（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回消息页（停留2s)')
            SeaOfStarsAW.ut_device.click(0.071, 0.093, 0.20)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.071, 0.093, 0.20)
            time.sleep(2)

            logging.info('24、点击我的（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击我的（停留2s)')
            SeaOfStarsAW.ut_device.click(0.896, 0.923, 0.20)
            time.sleep(2)

            logging.info('25、点击支付宝会员（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击支付宝会员（停留2s)')
            SeaOfStarsAW.ut_device.click(0.502, 0.249, 0.20)
            time.sleep(2)

            logging.info('26、上滑5次，下滑5次查看会员页（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '上滑5次，下滑5次查看会员页（停留2s)')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            logging.info('27、返回“我的”页（停留2s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回“我的”页（停留2s)')
            SeaOfStarsAW.ut_device.click(0.063, 0.091, 0.20)
            time.sleep(2)

            logging.info('28、点击账单(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击账单(停留1s)')
            SeaOfStarsAW.ut_device.click(0.485, 0.311, 0.20)
            time.sleep(1)

            logging.info('29、返回我的页(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回我的页(停留1s)')
            SeaOfStarsAW.ut_device.click(0.051, 0.091, 0.20)
            time.sleep(1)

            logging.info('30、点击余额(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击余额(停留1s)')
            SeaOfStarsAW.ut_device.click(0.485, 0.43, 0.20)
            time.sleep(1)

            logging.info('31、返回我的页(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回我的页(停留1s)')
            SeaOfStarsAW.ut_device.click(0.063, 0.089, 0.20)
            time.sleep(1)

            logging.info('32、点击设置(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击设置(停留1s)')
            SeaOfStarsAW.ut_device.click(0.931, 0.087, 0.20)
            time.sleep(1)

            logging.info('33、点击新消息通知(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击新消息通知(停留1s)')
            SeaOfStarsAW.ut_device.click(0.477, 0.405, 0.20)
            time.sleep(1)

            logging.info('34、返回设置页(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回设置页(停留1s)')
            SeaOfStarsAW.ut_device.click(0.057, 0.091, 0.20)
            time.sleep(1)

            logging.info('35、点击通用(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击通用(停留1s)')
            SeaOfStarsAW.ut_device.click(0.514, 0.642, 0.20)
            time.sleep(1)

            logging.info('36、返回我的页(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回我的页(停留1s)')
            SeaOfStarsAW.ut_device.click(0.057, 0.087, 0.20)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.057, 0.087, 0.20)
            time.sleep(1)

            logging.info('37、点击首页(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击首页(停留1s)')
            SeaOfStarsAW.ut_device.click(0.091, 0.926, 0.20)
            time.sleep(1)

            logging.info('38、返回home页面(停留1s)')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回home页面(停留1s)')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.alipay.iphoneclient')

        logging.info('用例执行结束')