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
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(2)

        for test_time in range(0, self.TEST_TIME):
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'step_' + str(test_time),
                self.screenshot_dir_path,
            )
            try:
                for step, (app_name, bundle_id) in enumerate(self.APP_LIST, start=1):
                    logging.info('%s、启动%s（%s），停留2s', step, app_name, bundle_id)
                    SeaOfStarsAW.trace_thread.add_log(app_name, '启动应用，停留2s')
                    try:
                        SeaOfStarsAW.ut_device.session().app_activate(bundle_id)
                        time.sleep(2)
                    finally:
                        SeaOfStarsAW.ut_device.home()
                    logging.info('%s、%s返回桌面', step, app_name)
                    SeaOfStarsAW.trace_thread.add_log(app_name, '返回桌面')
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
