import time

from aw import SeaOfStarsAW
from cases.dingding_common import DingTalkCase


class PerformanceDynamic_dingding_0020(DingTalkCase):
    """Excel 7.0.2：钉钉发起会议，切换头条浏览后返回结束会议。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动钉钉')
                self.start_dingtalk()
            self.step(2, '点击屏幕底部更多，拉起更多选项')
            self.open_more_panel()
            self.step(3, '点击会议，切换到会议详情页面')
            self.open_meeting_tab()
            self.step(4, '点击发起会议，选择语音会议')
            self.start_voice_meeting()
            self.step(5, '点击进入会议按钮，进入会议详情')
            self.enter_meeting()
            self.step(6, '滑动返回Home页')
            self.launcher()
            self.step(7, '启动今日头条')
            self.start_toutiao()
            self.step(8, '主页浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(9, '点击热榜tab')
            self.tap_headline_channel('热榜')
            self.step(10, '热榜浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(11, '点击热榜第一条')
            self.open_first_headline('热榜')
            self.step(12, '热榜第一条上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(13, '返回今日头条主界面')
            self.return_toutiao_home()
            self.step(14, '点击发现tab')
            self.tap_headline_channel('发现')
            self.step(15, '发现页浏览上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(16, '返回推荐页，点击第一条文章')
            self.tap_headline_channel('推荐')
            self.open_first_headline('推荐')
            self.step(17, '第一条文章上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(18, '返回今日头条主界面')
            self.return_toutiao_home()
            self.step(19, '滑动返回Home页')
            self.launcher()
            self.step(20, '启动钉钉')
            self.device.app_activate(self.PACKAGE)
            time.sleep(6)
            self.step(21, '点击今天列表下的第一个会议信息，点击入会')
            self.activate_dingtalk_meeting()
            self.step(22, '等待1min')
            time.sleep(60)
            self.step(23, '点击结束，点击全员结束会议，结束会议')
            self.end_meeting()
            self.step(24, '返回钉钉主界面')
            self.return_dingtalk_main()
            with self.capture_trace(iteration, 25):
                self.step(25, '滑动返回Home页')
                self.launcher()
