from aw import SeaOfStarsAW
from cases.taobao_common import TaobaoCase


class PerformanceDynamic_taobao_0020(TaobaoCase):
    """Excel 7.0.2：淘宝首页频道、视频和订单浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动淘宝')
                self.start_taobao()
            self.step(2, '点击推荐，切换到推荐页面')
            self.select_home_channel('推荐')
            self.step(3, '点击切换第三个tab图标页面')
            self.select_third_home_channel()
            self.step(4, '第三个tab图标页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '返回淘宝主界面')
            self.return_home()
            self.step(6, '推荐页面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(7, '点击关注，切换到关注页面')
            self.select_home_channel('关注')
            self.step(8, '关注页面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '点击tab栏逛逛，切换到逛页面')
            self.open_guangguang()
            self.step(10, '浏览逛逛页面，上滑5次，下滑5次，右滑3次，左滑3次')
            self.browse(5, 5)
            self.horizontal_browse(3, 3)
            self.step(11, '点击tab栏我的淘宝')
            self.open_my_taobao()
            self.step(12, '点击我的订单')
            self.open_my_orders()
            self.step(13, '浏览订单页面，左滑5次，右滑5次')
            self.horizontal_browse(0, 5)
            self.horizontal_browse(5, 0)
            self.step(14, '返回淘宝主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
