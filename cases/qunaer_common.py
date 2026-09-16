"""去哪儿旅行 iOS 动态性能用例公共能力。"""

import logging
import time
from contextlib import contextmanager

from cases.wda_case_common import WdaCase


class QunarCase(WdaCase):
    PACKAGE = 'com.qunar.iphoneclient8'
    APP_NAME = '去哪儿旅行'

    @contextmanager
    def capture_trace_5s(self, iteration, step_number):
        """只采集指定首尾步骤，并保证 trace 时长不少于 5 秒。"""
        with self.capture_trace(iteration, step_number):
            started_at = time.monotonic()
            try:
                yield
            finally:
                time.sleep(max(0, 5 - (time.monotonic() - started_at)))

    def prepare_iteration(self):
        try:
            self.device.app_terminate(self.PACKAGE)
        except Exception:
            logging.exception('结束去哪儿旅行进程失败，继续启动')
        time.sleep(1)

    def point(self, x_ratio, y_ratio):
        size = self.device.window_size()
        return round(size.width * x_ratio), round(size.height * y_ratio)

    def click_ratio(self, x_ratio, y_ratio, wait=2):
        self.device.click(*self.point(x_ratio, y_ratio))
        time.sleep(wait)

    def start_qunar(self):
        self.start_app(wait=7)
        self.dismiss_marketing_popup()

    def dismiss_marketing_popup(self):
        # 刮刮卡等营销弹窗没有可访问性节点；关闭点已在 402x874 实机核对。
        # 无弹窗时该点落在页面留白/广告区域，不会触发订单动作。
        self.click_ratio(0.913, 0.154, wait=1)

    def open_flight(self):
        self.click_ratio(0.179, 0.354, wait=6)
        self.dismiss_marketing_popup()

    def search_flight(self):
        self.click_ratio(0.500, 0.604, wait=10)

    def select_tomorrow(self):
        self.click_ratio(0.310, 0.149, wait=6)

    def scroll_to_top(self, count=6):
        for _ in range(count):
            self.device.swipe(0.5, 0.28, 0.5, 0.82, 0.25)
            time.sleep(0.5)

    def open_first_flight(self):
        self.click_ratio(0.500, 0.412, wait=8)

    def open_first_booking(self):
        self.click_ratio(0.873, 0.514, wait=7)

    def back_tap(self, count=1, wait=2):
        for _ in range(count):
            self.click_ratio(0.055, 0.085, wait=wait)

    def edge_back(self, count=1):
        for _ in range(count):
            self.device.swipe(0.01, 0.50, 0.92, 0.50, 0.35)
            time.sleep(2)

    def open_hotel(self):
        self.click_ratio(0.179, 0.276, wait=6)
        self.dismiss_marketing_popup()

    def choose_xian(self):
        self.click_ratio(0.149, 0.269, wait=4)
        # 城市列表是 RN 画布：先点右侧 X 索引，再点 X 区首行“西安”。
        self.click_ratio(0.963, 0.778, wait=4)
        self.click_ratio(0.373, 0.307, wait=5)

    def open_hotel_orders(self):
        self.click_ratio(0.853, 0.641, wait=5)

    def search_hotel(self):
        self.click_ratio(0.500, 0.492, wait=10)

    def open_first_hotel(self):
        self.scroll_to_top(count=5)
        self.click_ratio(0.500, 0.709, wait=9)

    def open_hotel_gallery(self):
        # 封面先进入“详情/设施”，再点该页第一张大图进入全屏图集。
        self.click_ratio(0.500, 0.286, wait=5)
        self.click_ratio(0.500, 0.572, wait=5)

    def horizontal_browse(self, left, right):
        for start, end, count in ((0.85, 0.15, left), (0.15, 0.85, right)):
            for _ in range(count):
                self.device.swipe(start, 0.50, end, 0.50, 0.35)
                time.sleep(0.7)

    def open_checkin_seat(self):
        # 机票首页上滑后，“值机选座”位于服务宫格第三项。
        self.device.swipe(0.5, 0.80, 0.5, 0.22, 0.55)
        time.sleep(3)
        self.click_ratio(0.612, 0.740, wait=8)

    def open_train(self):
        self.click_ratio(0.435, 0.354, wait=8)
        # 首次进入火车页会出现 12306 登录权益页；选择“放弃权益”可继续
        # 浏览，不登录、不注册，也不导入个人订单。
        try:
            abandon = self.device(name='放弃权益')
            if abandon.exists:
                abandon.click()
                time.sleep(8)
        except Exception:
            logging.exception('检查 12306 登录权益弹窗失败')

    def set_train_arrival_from_hot_city(self):
        # Qunar 的火车 RN 页面存在约 80pt 的点击纵向偏移。以下点位经
        # 当前 402x874 实机核对：打开“选择到达”，再选择热门城市“北京”。
        self.click_ratio(0.760, 0.400, wait=4)
        self.click_ratio(0.820, 0.463, wait=7)

    def search_train(self):
        self.click_ratio(0.500, 0.572, wait=12)
