import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qianwen_0010(Case):
    all_app_package_list = ['com.aliyun.ios.tongyi']
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
        SeaOfStarsAW.trace_thread.add_log('千问', description)

    def _ask(self, question, input_x, input_y, send_x, send_y):
        device = SeaOfStarsAW.ut_device
        device.click(input_x, input_y)
        time.sleep(1)
        device().set_text(question)
        time.sleep(1)
        send_button = device(labelContains='发送', timeout=2)
        if send_button.exists:
            send_button.click()
        else:
            logging.warning('未找到发送按钮，使用待校准坐标：%s', (send_x, send_y))
            device.click(send_x, send_y)
        time.sleep(10)

    def _browse_answer(self):
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """千问连续提问并浏览三次回答。"""
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
                self._log_step('1、启动千问')
                device.app_activate('com.aliyun.ios.tongyi')
                time.sleep(5)

                self._log_step('2、点击对话框，输入什么是AI')
                self._ask('什么是AI', 0.45, 0.90, 0.92, 0.90)

                self._log_step('3、浏览搜索结果，上下滑动3次')
                self._browse_answer()

                self._log_step('4、点击对话框，输入华为终端的主要产品有哪些')
                self._ask(
                    '华为终端的主要产品有哪些',
                    0.45,
                    0.90,
                    0.92,
                    0.90,
                )

                self._log_step('5、浏览搜索结果，上下滑动3次')
                self._browse_answer()

                self._log_step('6、点击对话框，输入介绍几款市面上主流的手机')
                self._ask(
                    '介绍几款市面上主流的手机',
                    0.45,
                    0.90,
                    0.92,
                    0.90,
                )

                self._log_step('7、浏览搜索结果，上下滑动3次')
                self._browse_answer()

                self._log_step('8、返回千问主界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('9、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
