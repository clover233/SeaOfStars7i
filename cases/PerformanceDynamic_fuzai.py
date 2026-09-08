import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fuzai(Case):
    APP_LIST = [
        ('天天象棋', 'com.tencent.qqchschess'),
        ('掼蛋', 'com.zhanlang.swgd66'),
        ('途游斗地主（比赛版）', 'com.tuyoo.doudizhu.3d'),
        ('多乐够级', 'com.7k7k.gouji'),
        ('钱包', 'com.apple.Passbook'),
        ('起点读书', 'm.qidian.QDReaderAppStore'),
        ('央广网', 'com.wang.CNRNewMediaApp'),
        ('酷狗音乐', 'com.kugou.kugou1002'),
        ('新浪新闻', 'com.sina.sinanews'),
        ('天天爱消除', 'com.tencent.peng'),
        ('凤凰新闻', 'ifengNews'),
        ('搜狐新闻', 'com.sohu.newspaper'),
        ('蜻蜓FM', 'com.Qting.QTTour'),
        ('懒人听书', 'com.yytingting.iting'),
        ('YY', 'yyvoice'),
        ('地铁跑酷', 'com.kiloo.subwaysurf.cn'),
    ]
    all_app_package_list = [bundle_id for _, bundle_id in APP_LIST]
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        # 钱包是系统应用，不依赖第三方应用列表检查，由实际启动确认可用性。
        # 保留后台应用，累积负载。
        return True

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        按顺序打开16个应用，每个应用停留2秒后返回桌面，保留后台负载。
        """
        logging.info("用例开始执行")

        for test_time in range(0, self.TEST_TIME):
            # 1、启动支付宝
            logging.info('1、启动支付宝')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '启动支付宝')
            SeaOfStarsAW.ut_device.app_activate('com.alipay.iphoneclient')
            time.sleep(2)
            time.sleep(1)

            # 2、点击出行
            logging.info('2、点击出行')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击出行')
            SeaOfStarsAW.ut_device.click(0.623, 0.155, 0.2)
            time.sleep(2)

            # 3、切换地铁页
            logging.info('3、切换地铁页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '切换地铁页')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(1)

            # 4、返回上一页
            logging.info('返回上一页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回上一页')
            SeaOfStarsAW.ut_device.click(0.054, 0.088, 0.2)
            time.sleep(1)

            # 5、点击卡包
            logging.info('点击卡包')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击卡包')
            SeaOfStarsAW.ut_device.click(0.873, 0.151, 0.2)
            time.sleep(2)

            # 5、返回上一页
            logging.info('5、返回上一页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回上一页')
            SeaOfStarsAW.ut_device.click(0.054, 0.088, 0.2)
            time.sleep(1)

            # 6、点击我的
            logging.info('6、点击我的')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '点击我的')
            SeaOfStarsAW.ut_device.click(0.893, 0.922, 0.2)
            time.sleep(1)

            # 7、切回支付宝主页面
            logging.info('7、切回支付宝主页面')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '切回支付宝主页面')
            SeaOfStarsAW.ut_device.click(0.091, 0.919, 0.2)
            time.sleep(1)

            # 8、收付款
            logging.info('8、收付款')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '收付款')
            SeaOfStarsAW.ut_device.click(0.373, 0.155, 0.2)
            time.sleep(1)

            # 9、转账
            logging.info('9、转账')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '转账')
            SeaOfStarsAW.ut_device.click(0.261, 0.875, 0.2)
            time.sleep(1)

            # 10、转到银行卡
            logging.info('10、转到银行卡')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '转到银行卡')
            SeaOfStarsAW.ut_device.click(0.511, 0.257, 0.2)
            time.sleep(1)

            # 11、返回上一页
            logging.info('11、返回上一页')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回上一页')
            SeaOfStarsAW.ut_device.click(0.057, 0.085, 0.2)
            time.sleep(1)

            # 12、转到支付宝
            logging.info('12、转到支付宝')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '转到支付宝')
            SeaOfStarsAW.ut_device.click(0.192, 0.258, 0.2)
            time.sleep(1)

            # 13、返回支付宝主界面
            logging.info('13、返回支付宝主界面')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回支付宝主界面')
            SeaOfStarsAW.ut_device.click(0.054, 0.095, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.057, 0.087, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.048, 0.091, 0.2)
            time.sleep(1)

            # 14、首页——扫一扫
            logging.info('14、首页——扫一扫')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '首页——扫一扫')
            SeaOfStarsAW.ut_device.click(0.123, 0.153, 0.2)
            time.sleep(1)
            logging.info('相册')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '相册')
            SeaOfStarsAW.ut_device.click(0.87, 0.809, 0.2)
            time.sleep(1)
            logging.info('第一张图')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '第一张图')
            SeaOfStarsAW.ut_device.click(0.126, 0.157, 0.2)
            time.sleep(1)

            # 15、返回支付宝主界面
            logging.info('15、返回支付宝主界面')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回支付宝主界面')
            SeaOfStarsAW.ut_device.click(0.08, 0.096, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.08, 0.096, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.08, 0.096, 0.2)
            time.sleep(1)

            # 16、返回home界面
            logging.info('16、返回Home界面')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回Home界面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.alipay.iphoneclient')

        logging.info('用例执行结束')
