from aw import SeaOfStarsAW
from cases.dingding_common import DingTalkCase


class PerformanceDynamic_dingding_0010(DingTalkCase):
    """Excel 7.0.2：钉钉浏览群消息并发送文本。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动钉钉')
                self.start_dingtalk()
            self.step(2, '点击左下角的消息图标，切换到消息页')
            self.tap('消息', min_y=750, wait=3)
            self.step(3, '点击欢迎试用钉钉群')
            self.open_welcome_group()
            self.step(4, '群消息页面，上滑2次、下滑2次')
            self.browse(2, 2)
            self.step(5, '点击底部消息输入框，输入你好，点击发送')
            self.send_group_text('你好')
            self.step(6, '点击右上角的更多，切换到更多页面')
            self.open_group_info()
            self.step(7, '更多页面浏览，上滑1次、下滑1次')
            self.browse(1, 1)
            self.step(8, '返回钉钉主界面')
            self.return_messages()
            with self.capture_trace(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
