import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Photo_0030(Case):
    # tidevice applist 可能不返回系统应用，因此不在 set_up 中校验包名。
    all_app_package_list = []
    TEST_TIME = 1
    APP_PACKAGE = 'com.apple.mobileslideshow'
    ALBUM_NAME = '动态测试'

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

    def _click_any(self, labels, x, y, contains=False):
        if isinstance(labels, str):
            labels = (labels,)
        for label in labels:
            selector_args = {
                'labelContains' if contains else 'label': label,
                'timeout': 1,
            }
            element = SeaOfStarsAW.ut_device(**selector_args)
            if element.exists:
                element.click()
                time.sleep(2)
                return
        logging.warning('未找到控件%s，使用待校准坐标：%s', labels, (x, y))
        SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(2)

    def _swipe_back(self):
        SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
        time.sleep(2)

    def _browse_fling(self, count):
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

    def _browse_follow(self, count):
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.2, duration=0.8)
            time.sleep(1)
        for _ in range(count):
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, duration=0.8)
            time.sleep(1)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """图库浏览照片和视频相册，并新建、删除测试相册。"""
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

                self._log_step('2、点击相册，切换到相册页')
                self._click_any('相册', 0.7, 0.95)

                self._log_step('3、点击图片进入图片相册页')
                self._click_any(('图片', '所有照片'), 0.25, 0.25, contains=True)

                self._log_step('4、图片相册页向上抛滑5次、向下抛滑5次')
                self._browse_fling(5)

                self._log_step('5、图片相册页向上跟手滑5次、向下跟手滑5次')
                self._browse_follow(5)

                self._log_step('6、进入图片相册后侧滑返回相册页，重复5次')
                self._swipe_back()
                for _ in range(5):
                    self._click_any(
                        ('图片', '所有照片'),
                        0.25,
                        0.25,
                        contains=True,
                    )
                    self._swipe_back()

                self._log_step('7、点击视频，进入视频相册页')
                self._click_any('视频', 0.75, 0.25, contains=True)

                self._log_step('8、点击第一个视频查看详情')
                device.click(0.18, 0.25)
                time.sleep(2)

                self._log_step('9、点击删除图标，并在提示框中确认删除')
                device.click(0.92, 0.92)
                time.sleep(1)
                self._click_any(('删除视频', '删除'), 0.90, 0.08, contains=True)

                self._log_step('10、返回相册界面')
                self._swipe_back()

                self._log_step('11、点击新建，拉起新建相册提示')
                self._click_any(('新建相册', '新建'), 0.92, 0.08, contains=True)

                self._log_step('12、设置新建相册名称为动态测试后确认')
                device().set_text(self.ALBUM_NAME)
                time.sleep(1)
                self._click_any(('存储', '保存', '完成', '好'), 0.90, 0.08)

                self._log_step('13、浏览拉起的图片和视频tab，上滑5次、下滑5次')
                self._click_any(('照片', '图片'), 0.25, 0.25)
                self._browse_fling(5)
                self._click_any('视频', 0.75, 0.25)
                self._browse_fling(5)

                self._log_step('14、选择第一个文件后，点击X号')
                device.click(0.18, 0.25)
                time.sleep(1)
                self._click_any(('关闭', '取消'), 0.95, 0.08)

                self._log_step('15、长按动态测试相册后删除相册，并确认删除')
                album = device(label=self.ALBUM_NAME, timeout=2)
                if album.exists:
                    center = album.bounds.center
                    device.tap_hold(center.x, center.y, duration=2)
                else:
                    logging.warning('未找到动态测试相册，使用待校准坐标：%s',
                                    (0.25, 0.25))
                    device.tap_hold(0.25, 0.25, duration=2)
                time.sleep(2)
                self._click_any('删除相册', 0.90, 0.08, contains=True)
                self._click_any('删除', 0.90, 0.08)

                self._log_step('16、返回图库主界面')
                albums = device(label='相册', timeout=2)
                if albums.exists:
                    albums.click()
                    time.sleep(2)
                else:
                    self._swipe_back()

                self._log_step('17、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
