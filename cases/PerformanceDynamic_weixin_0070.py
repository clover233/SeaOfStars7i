from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0070(WeixinCase):
    """Excel 7.0.2：瑞幸咖啡小程序菜单与加购。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '下滑调出最近小程序')
            self.open_recent_mini_programs()
            self.step(3, '打开瑞幸咖啡小程序')
            self.open_common_mini_program(self.LUCKIN_MINI)
            self.step(4, '点击菜单')
            self.open_luckin_menu()
            self.step(5, '点击人气Top')
            self.tap('人气Top', contains=True, min_y=100, max_y=760, wait=3)
            self.step(6, '点击第一个预置商品')
            self.open_luckin_first_product()
            self.step(7, '加入购物车')
            self.tap('加入购物车', min_y=700, wait=3)
            self.step(8, '返回微信主界面')
            self.close_mini_program()
            with self.capture_trace_5s(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
