from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0100(WeixinCase):
    """Excel 7.0.2：视频号、直播与游戏浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击发现')
            self.tap('发现', min_y=760, wait=2)
            self.step(3, '点击视频号')
            self.tap('视频号', min_y=80, max_y=300, wait=5)
            self.dismiss_content_prompts()
            self.step(4, '上滑6次浏览视频号')
            self.browse(6, 0)
            self.step(5, '返回发现页')
            self.return_discover()
            self.step(6, '点击直播')
            self.tap('直播', min_y=100, max_y=360, wait=5)
            self.dismiss_content_prompts()
            self.step(7, '点击第一个直播')
            self.open_first_live()
            self.step(8, '上滑6次切换浏览直播')
            self.browse(6, 0)
            self.step(9, '返回发现页')
            self.return_discover()
            self.step(10, '点击游戏')
            self.tap('游戏', min_y=450, max_y=740, wait=6)
            self.dismiss_content_prompts()
            self.step(11, '游戏首页上滑6次、下滑6次')
            self.browse(6, 6)
            self.step(12, '返回发现页')
            self.return_discover()
            self.step(13, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
