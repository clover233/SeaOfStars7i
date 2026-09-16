from aw import SeaOfStarsAW
from cases.jingdong_common import JingdongCase


class PerformanceDynamic_jingdong_0040(JingdongCase):
    """京东直播互动及订单浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动京东')
                self.start_jingdong()
            self.step(2, '点击逛后点击直播')
            self.open_live_list()
            self.step(3, '浏览直播页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(4, '点击第一个直播间进入')
            self.open_first_live()
            self.step(5, '点击底部输入框')
            self.focus_live_comment()
            self.step(6, '输入不错并发送')
            self.send_live_comment('不错')
            self.step(7, '点击右下角购物袋图标')
            self.open_live_bag()
            self.step(8, '浏览购物袋，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '返回京东主界面')
            self.return_home()
            self.step(10, '点击我的')
            self.bottom_tab('我的')
            self.step(11, '点击全部订单')
            self.tap('全部订单', '全部', contains=True, wait=5)
            self.step(12, '浏览全部订单页面，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(13, '点击待收货')
            self.tap('待收货', contains=True, wait=4)
            self.step(14, '返回京东主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
