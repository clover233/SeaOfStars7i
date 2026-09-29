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
        """按顺序打开16个应用，每个应用动作各采集一份 trace。"""
        logging.info("用例开始执行")
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(3)

        app_packages = [
            'com.tencent.qqchschess',
            'com.zhanlang.swgd66',
            'com.tuyoo.doudizhu.3d',
            'com.7k7k.gouji',
            'com.apple.Passbook',
            'm.qidian.QDReaderAppStore',
            'com.wang.CNRNewMediaApp',
            'com.kugou.kugou1002',
            'com.sina.sinanews',
            'com.tencent.peng',
            'ifengNews',
            'com.sohu.newspaper',
            'com.Qting.QTTour',
            'com.yytingting.iting',
            'yyvoice',
            'com.kiloo.subwaysurf.cn',
        ]
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        for iteration in range(self.TEST_TIME):
            for step_number, package in enumerate(app_packages, 1):
                step_text = '{}、启动 {}'.format(step_number, package)
                try:
                    SeaOfStarsAW.start_trace(
                        self.trace_dir_path,
                        self.__class__.__name__,
                        'step_{}'.format(step_number),
                        self.screenshot_dir_path,
                    )
                    logging.info(step_text)
                    SeaOfStarsAW.trace_thread.add_log('负载', step_text)
                    SeaOfStarsAW.ut_device.app_activate(package)
                    time.sleep(3)
                    SeaOfStarsAW.ut_device.home()
                finally:
                    SeaOfStarsAW.stop_trace()
        logging.info('用例执行结束')
