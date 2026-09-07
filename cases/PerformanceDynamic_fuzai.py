import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fuzai(Case):
    all_app_package_list = ['']
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
        按顺序打开16个应用，每个应用停留3秒后返回桌面，保留后台负载。
        仅采集天天象棋和地铁跑酷从启动到返回桌面的两段trace。
        """
        logging.info("用例开始执行")
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(3)

        for test_time in range(0, self.TEST_TIME):
            step = 0
            try:
                SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                         self.screenshot_dir_path)
                logging.info('1、起负载')
                SeaOfStarsAW.trace_thread.add_log('负载', '起负载')
                SeaOfStarsAW.ut_device.app_activate('com.tencent.qqchschess')
                time.sleep(3)
                SeaOfStarsAW.ut_device.home()

            finally:
                SeaOfStarsAW.stop_trace()

            SeaOfStarsAW.ut_device.app_activate('com.zhanlang.swgd66')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.tuyoo.doudizhu.3d')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.7k7k.gouji')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.apple.Passbook')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('m.qidian.QDReaderAppStore')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.wang.CNRNewMediaApp')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.kugou.kugou1002')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.sina.sinanews')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.tencent.peng')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('ifengNews')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.sohu.newspaper')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.Qting.QTTour')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('com.yytingting.iting')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            SeaOfStarsAW.ut_device.app_activate('yyvoice')
            time.sleep(3)
            SeaOfStarsAW.ut_device.home()

            step = 1
            try:
                SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                         self.screenshot_dir_path)
                SeaOfStarsAW.trace_thread.add_log('负载', '地铁跑酷')
                SeaOfStarsAW.ut_device.app_activate('com.kiloo.subwaysurf.cn')
                time.sleep(3)
                SeaOfStarsAW.ut_device.home()
            finally:
                SeaOfStarsAW.stop_trace()
        logging.info('用例执行结束')
