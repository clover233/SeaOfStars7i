import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weixin_0040(Case):
    all_app_package_list = ['com.tencent.xin']
    TEST_TIME = 1
    APP_PACKAGE = 'com.tencent.xin'

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
        SeaOfStarsAW.trace_thread.add_log('微信', description)

    def _click(self, label, x, y, contains=False, wait=2):
        selector_args = {
            'labelContains' if contains else 'label': label,
            'timeout': 2,
        }
        element = SeaOfStarsAW.ut_device(**selector_args)
        if element.exists:
            element.click()
        else:
            logging.warning('未找到控件“%s”，使用待校准坐标：%s', label, (x, y))
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(wait)

    def _click_any(self, labels, x, y, contains=False, wait=2):
        for label in labels:
            selector_args = {
                'labelContains' if contains else 'label': label,
                'timeout': 1,
            }
            element = SeaOfStarsAW.ut_device(**selector_args)
            if element.exists:
                element.click()
                time.sleep(wait)
                return
        logging.warning('未找到控件%s，使用待校准坐标：%s', labels, (x, y))
        SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(wait)

    def _browse(self, up_count, down_count=None):
        down_count = up_count if down_count is None else down_count
        for _ in range(up_count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(down_count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    def _start_trace(self, test_time):
        SeaOfStarsAW.start_trace(
            self.trace_dir_path,
            self.__class__.__name__,
            'step_' + str(test_time),
            self.screenshot_dir_path,
        )

    def _launch_weixin(self):
        SeaOfStarsAW.ut_device.app_activate(self.APP_PACKAGE)
        time.sleep(5)

    def _return_home(self):
        SeaOfStarsAW.swipe_to_launcher()
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """微信发送文字、语音、表情，并发起视频和语音通话。"""
        logging.info('用例开始执行')
        device = SeaOfStarsAW.ut_device
        if device.locked():
            device.unlock()
            time.sleep(2)

        for test_time in range(self.TEST_TIME):
            self._start_trace(test_time)
            try:
                self._log_step('1、启动微信')
                self._launch_weixin()

                self._log_step('2、点击测试账号，进入好友聊天页面')
                self._click('文件传输助手', 0.5, 0.20)

                self._log_step('3、点击输入框，进入消息编辑界面')
                device.click(0.45, 0.91)
                time.sleep(1)

                self._log_step('4、输入哈哈哈，点击发送')
                device().set_text('哈哈哈')
                time.sleep(1)
                self._click('发送', 0.90, 0.91)

                self._log_step('5、点击语音按钮，发送语音给好友')
                device.click(0.07, 0.93)
                time.sleep(1)
                voice_button = device(labelContains='按住说话', timeout=2)
                if voice_button.exists:
                    center = voice_button.bounds.center
                    device.tap_hold(center.x, center.y, duration=3)
                else:
                    device.tap_hold(0.50, 0.93, duration=3)
                time.sleep(2)

                self._log_step('6、点击表情包按钮，进入表情框界面')
                device.click(0.86, 0.93)
                time.sleep(2)

                self._log_step('7、选择前三个表情，点击发送')
                device.click(0.10, 0.72)
                device.click(0.25, 0.72)
                device.click(0.40, 0.72)
                time.sleep(1)
                self._click('发送', 0.90, 0.93)

                self._log_step('8、点击加号按钮，进入更多功能页面')
                device.click(0.95, 0.93)
                time.sleep(2)

                self._log_step('9、点击视频通话，进入选择通话界面')
                self._click('视频通话', 0.25, 0.72)

                self._log_step('10、点击视频通话，进入视频通话界面')
                self._click('视频通话', 0.50, 0.72)
                time.sleep(5)

                self._log_step('11、点击挂断按钮，返回好友聊天页面')
                self._click_any(('挂断', '结束'), 0.50, 0.86, contains=True)

                self._log_step('12、点击加号按钮，进入更多功能页面')
                device.click(0.95, 0.93)
                time.sleep(2)

                self._log_step('13、点击视频通话，进入选择通话界面')
                self._click('视频通话', 0.25, 0.72)

                self._log_step('14、点击语音通话，进入语音通话界面')
                self._click('语音通话', 0.50, 0.65)
                time.sleep(5)

                self._log_step('15、点击挂断按钮，返回好友聊天页面')
                self._click_any(('挂断', '结束'), 0.50, 0.86, contains=True)

                self._log_step('16、返回微信主界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('17、滑动返回Home页')
                self._return_home()
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
