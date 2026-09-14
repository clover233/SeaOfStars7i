import time

from aw import SeaOfStarsAW
from cases.qq_common import QqCase


class PerformanceDynamic_qq_0010(QqCase):
    """Excel 7.0.2：浏览空间动态及好友动态图片。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动QQ')
                self.start_qq()
            self.step(2, '点击动态，进入动态页面')
            dynamic = self.bottom_tab('动态')
            if dynamic is None:
                self.fail('未找到 QQ 底部动态页签')
            self.tap_node(dynamic)
            time.sleep(4)
            self.step(3, '点击空间动态，进入空间动态页面')
            self.tap('空间动态', min_y=120, max_y=400, wait=6)
            self.step(4, '浏览空间动态，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '空间动态页面查看好友动态图片')
            self.open_space_picture()
            self.step(6, '图片浏览，横向滑动3次')
            self.swipe_images(0, 3)
            self.step(7, '返回QQ主界面')
            self.return_message_home()
            with self.capture_trace(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
