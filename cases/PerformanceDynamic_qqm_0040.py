import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qqm_0040(Case):
    all_app_package_list = ['com.tencent.QQMusic']
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for package in self.all_app_package_list:
            if package not in phone_app_list:
                raise RuntimeError('未安装测试应用：{}'.format(package))
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('QQ音乐', description)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """QQ音乐首页浏览并播放音乐卡片。"""
        logging.info('用例开始执行')
        device = SeaOfStarsAW.ut_device
        if device.locked():
            device.unlock()
            time.sleep(2)

        for test_time in range(self.TEST_TIME):
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'step_' + str(test_time),
                self.screenshot_dir_path,
            )
            try:
                self._log_step('1、启动QQ音乐')
                device.app_activate('com.tencent.QQMusic')
                time.sleep(5)

                self._log_step('2、浏览首页，上滑2次、下滑2次')
                for _ in range(2):
                    device.swipe_up()
                    time.sleep(1)
                for _ in range(2):
                    device.swipe_down()
                    time.sleep(1)

                self._log_step('3、点击一个音乐卡片进行播放')
                device.click(0.5, 0.35)
                time.sleep(5)

                self._log_step('4、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
