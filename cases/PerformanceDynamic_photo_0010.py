import time

from aw import SeaOfStarsAW
from cases.photo_common import PhotoCase


class PerformanceDynamic_photo_0010(PhotoCase):
    """Excel 7.0.2: browse the Photos library and inspect photos."""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动图库')
                self.start_photos()

            self.step(2, '点击照片，进入照片 tab 页')
            self.open_library()
            self.ensure_minimum_photos(6)
            self.normalize_day_view()

            self.step(3, '切换年/月/日视图，重复5次')
            self.cycle_library_scale(count=5)

            self.step(4, '捏合与捏开切换日/月/年缩放层级，重复5次')
            self.cycle_library_scale(count=5)

            self.step(5, '日视图向上抛滑5次，向下抛滑5次')
            self.fling_library(5, 5)

            self.step(6, '日视图向上跟手滑5次，向下跟手滑5次')
            self.drag_library(5, 5)

            self.step(7, '日视图向上拖动滚动条5次，向下拖动滚动5次')
            self.drag_library_scrollbar(5, 5)

            self.step(8, '点击查看第一张照片，进入大图')
            self.open_first_library_photo()

            self.step(9, '点击底部图片预览条，向右滑动3次')
            self.swipe_preview_strip('right', 3)

            self.step(10, '点击底部图片预览条，向左滑动3次')
            self.swipe_preview_strip('left', 3)

            self.step(11, '点击左上角按钮退出到照片页')
            self.leave_one_up()

            self.step(12, '打开第一张照片并点击返回，重复5次')
            for _ in range(5):
                self.open_first_library_photo()
                self.leave_one_up()

            self.step(13, '打开第一张照片并侧滑退出，重复5次')
            for _ in range(5):
                self.open_first_library_photo()
                self.edge_back_from_one_up()

            self.step(14, '点击第一张照片查看大图')
            self.open_first_library_photo()

            self.step(15, '左滑5次查看大图，右滑5次查看大图')
            size = self.device.window_size()
            for start, end, count in ((0.85, 0.15, 5), (0.15, 0.85, 5)):
                for _ in range(count):
                    self.device.swipe(round(size.width * start),
                                      round(size.height * 0.5),
                                      round(size.width * end),
                                      round(size.height * 0.5), 0.3)
                    time.sleep(0.6)

            self.step(16, '返回图库主界面')
            self.leave_one_up()
            self.return_to_library_main()

            with self.capture_trace_5s(iteration, 17):
                self.step(17, '滑动返回 Home 页')
                self.launcher()
