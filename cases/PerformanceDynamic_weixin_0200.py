from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0200(WeixinCase):
    """Excel 7.0.2：微信收藏与存储空间页面。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击我，切换到我页面')
            self.tap('我', min_y=760, wait=3)
            self.step(3, '点收藏，切换到收藏页面')
            self.tap('收藏', min_y=250, max_y=450, wait=4)
            self.step(4, '收藏页面上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(5, '点击第一条收藏，进入详情页')
            self.open_first_favorite()
            self.step(6, '返回微信我页面')
            self.return_me_page()
            self.step(7, '点击设置，切换到设置页面')
            self.tap('设置', min_y=450, max_y=700, wait=3)
            self.step(8, '点击通用，切换到通用页面')
            self.open_general_settings()
            self.step(9, '点击存储空间，切换到存储空间页面')
            self.tap('存储空间', min_y=400, max_y=700, wait=8)
            self.step(10, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
