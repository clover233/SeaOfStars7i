from aw import SeaOfStarsAW
from cases.phone_common import PhoneCase


class PerformanceDynamic_call_0020(PhoneCase):
    """Excel 7.0.2：输入并删除号码后浏览通话记录。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动电话')
                self.start_phone()
            self.step(2, '点击电话，查看所有通话')
            self.open_tab('通话')
            self.step(3, '输入号码10086后，删除键删除号码')
            self.enter_and_delete_number('10086')
            self.step(4, '点击拨号键盘上方空白处')
            self.show_call_history()
            self.step(5, '上滑5次，下滑5次，浏览拨打历史记录页面')
            self.browse(5, 5)
            with self.capture_trace(iteration, 6):
                self.step(6, '滑动返回Home页')
                self.launcher()
