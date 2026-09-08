import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Photo_0010(Case):
    # tidevice applist 可能不返回系统应用，因此不在 set_up 中校验包名。
    all_app_package_list = []
    TEST_TIME = 1
    APP_PACKAGE = 'com.apple.mobileslideshow'

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('图库', description)

    def _click(self, label, x, y):
        element = SeaOfStarsAW.ut_device(label=label, timeout=2)
        if element.exists:
            element.click()
        else:
            logging.warning('未找到控件“%s”，使用待校准坐标：%s',
                            label, (x, y))
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(1)

    def _back_button(self, x, y):
        back = SeaOfStarsAW.ut_device(labelContains='返回', timeout=2)
        if back.exists:
            back.click()
        else:
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(1)

    def _swipe_back(self):
        SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
        time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """图库照片视图切换、缩放和大图浏览。"""
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
                self._log_step('1、启动图库')
                device.app_activate(self.APP_PACKAGE)
                time.sleep(3)

                self._log_step('2、点击照片，进入照片tab页')
                self._click('照片', 0.1, 0.95)

                self._log_step('3、依次切换年、月、日视图，重复5次')
                for _ in range(5):
                    self._click('年', 0.2, 0.12)
                    self._click('月', 0.5, 0.12)
                    self._click('日', 0.8, 0.12)

                self._log_step('4、捏合切换日/月/年视图，再捏开切回日视图，重复5次')
                gallery = device(className='Application', timeout=2).get()
                for _ in range(5):
                    gallery.pinch(scale=0.5, velocity=-1)
                    time.sleep(1)
                    gallery.pinch(scale=0.5, velocity=-1)
                    time.sleep(1)
                    gallery.pinch(scale=2.0, velocity=1)
                    time.sleep(1)
                    gallery.pinch(scale=2.0, velocity=1)
                    time.sleep(1)

                self._log_step('5、日视图向上抛滑5次、向下抛滑5次')
                for _ in range(5):
                    device.swipe_up()
                    time.sleep(1)
                for _ in range(5):
                    device.swipe_down()
                    time.sleep(1)

                self._log_step('6、日视图向上跟手滑5次、向下跟手滑5次')
                for _ in range(5):
                    device.swipe(0.5, 0.8, 0.5, 0.2, duration=0.8)
                    time.sleep(1)
                for _ in range(5):
                    device.swipe(0.5, 0.2, 0.5, 0.8, duration=0.8)
                    time.sleep(1)

                self._log_step('7、日视图向上滚动条滑5次、向下滚动条滑5次')
                for _ in range(5):
                    device.swipe(0.98, 0.8, 0.98, 0.2, duration=1.0)
                    time.sleep(1)
                for _ in range(5):
                    device.swipe(0.98, 0.2, 0.98, 0.8, duration=1.0)
                    time.sleep(1)

                self._log_step('8、点击查看第一张照片，进入大图')
                device.click(0.18, 0.25)
                time.sleep(2)

                self._log_step('9、点击底部图片预览条，向右滑动3次')
                device.click(0.5, 0.92)
                time.sleep(1)
                for _ in range(3):
                    device.swipe(0.2, 0.92, 0.8, 0.92, duration=0.5)
                    time.sleep(1)

                self._log_step('10、点击底部图片预览条，向左滑动3次')
                device.click(0.5, 0.92)
                time.sleep(1)
                for _ in range(3):
                    device.swipe(0.8, 0.92, 0.2, 0.92, duration=0.5)
                    time.sleep(1)

                self._log_step('11、点击左上角按钮退出到照片页')
                self._back_button(0.05, 0.08)

                self._log_step('12、打开第一张照片后点击左上角退出，重复5次')
                for _ in range(5):
                    device.click(0.18, 0.25)
                    time.sleep(1)
                    self._back_button(0.05, 0.08)

                self._log_step('13、打开第一张照片后侧滑退出，重复5次')
                for _ in range(5):
                    device.click(0.18, 0.25)
                    time.sleep(1)
                    self._swipe_back()

                self._log_step('14、点击第一张照片查看大图')
                device.click(0.18, 0.25)
                time.sleep(2)

                self._log_step('15、左滑5次、右滑5次查看大图')
                for _ in range(5):
                    device.swipe_left()
                    time.sleep(1)
                for _ in range(5):
                    device.swipe_right()
                    time.sleep(1)

                self._log_step('16、返回图库主界面')
                self._back_button(0.05, 0.08)

                self._log_step('17、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
