import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Setting_0010(Case):
    # tidevice applist 可能不返回系统应用，因此不在 set_up 中校验包名。
    all_app_package_list = []
    TEST_TIME = 1
    APP_PACKAGE = 'com.apple.Preferences'

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('设置', description)

    def _click(self, label, x, y, contains=True):
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
        time.sleep(2)

    def _browse(self, count):
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """设置页面、主题、存储和电池浏览。"""
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
                self._log_step('1、启动设置')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('2、设置首页上滑2次、下滑2次')
                self._browse(2)

                self._log_step('3、点击华为账号，进入华为账号页面')
                self._click('华为账号', 0.5, 0.16)

                self._log_step('4、返回设置主页面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('5、点击进入关于手机页面')
                self._click('关于手机', 0.5, 0.82)

                self._log_step('6、返回设置主页面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('7、点击WLAN')
                self._click('WLAN', 0.5, 0.25, contains=False)

                self._log_step('8、WLAN页面上滑1次、下滑1次')
                self._browse(1)

                self._log_step('9、返回设置首页')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('10、点击显示和亮度')
                self._click('显示和亮度', 0.5, 0.42)

                self._log_step('11、亮度进度条向右拖动一次，再向左拖动一次')
                device.swipe(0.25, 0.35, 0.85, 0.35, duration=1.0)
                time.sleep(2)
                device.swipe(0.85, 0.35, 0.25, 0.35, duration=1.0)
                time.sleep(2)

                self._log_step('12、返回设置首页')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('13、点击声音和振动')
                self._click('声音和振动', 0.5, 0.50)

                self._log_step('14、点击信息铃声')
                self._click('信息铃声', 0.5, 0.42)

                self._log_step('15、铃声页面上滑2次、下滑2次')
                self._browse(2)

                self._log_step('16、返回设置首页')
                for _ in range(2):
                    device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                    time.sleep(2)

                self._log_step('17、点击桌面和个性化')
                self._click('桌面和个性化', 0.5, 0.58)

                self._log_step('18、点击更多主题')
                self._click('更多主题', 0.5, 0.30)

                self._log_step('19、点击萌主跳跳')
                self._click('萌主跳跳', 0.25, 0.35)

                self._log_step('20、点击应用')
                self._click('应用', 0.5, 0.90, contains=False)
                time.sleep(6)

                self._log_step('21、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)

                self._log_step('22、桌面左滑3次、右滑3次')
                for _ in range(3):
                    device.swipe_left()
                    time.sleep(1)
                for _ in range(3):
                    device.swipe_right()
                    time.sleep(1)

                self._log_step('23、启动设置')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('24、点击更多主题')
                self._click('更多主题', 0.5, 0.30)

                self._log_step('25、点击萌主嘿嘿')
                self._click('萌主嘿嘿', 0.75, 0.35)

                self._log_step('26、点击应用')
                self._click('应用', 0.5, 0.90, contains=False)
                time.sleep(6)

                self._log_step('27、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)

                self._log_step('28、桌面左滑3次、右滑3次')
                for _ in range(3):
                    device.swipe_left()
                    time.sleep(1)
                for _ in range(3):
                    device.swipe_right()
                    time.sleep(1)

                self._log_step('29、启动设置')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('30、返回设置主界面')
                for _ in range(3):
                    if device(label='WLAN', timeout=1).exists:
                        break
                    device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                    time.sleep(2)

                self._log_step('31、点击存储，进入存储页面')
                self._click('存储', 0.5, 0.72)

                self._log_step('32、存储页面上滑2次、下滑2次')
                self._browse(2)

                self._log_step('33、返回设置主界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('34、点击电池，进入电池页面')
                self._click('电池', 0.5, 0.80)

                self._log_step('35、返回设置主界面')
                device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
                time.sleep(2)

                self._log_step('36、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
