import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qqm_0050(Case):
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
        """QQ音乐首页暂停当前播放。"""
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

                self._log_step('2、QQ音乐首页点击底部暂停按钮')
                pause_button = device(labelContains='暂停', timeout=2)
                if pause_button.exists:
                    pause_button.click()
                else:
                    logging.warning('未找到暂停按钮，使用待校准坐标：%s', (0.90, 0.84))
                    device.click(0.90, 0.84)
                time.sleep(2)

                self._log_step('3、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
