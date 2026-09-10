from aw import SeaOfStarsAW
from cases.phone_common import PhoneCase


class PerformanceDynamic_call_0010(PhoneCase):
    """Excel 7.0.2：浏览电话联系人并打开搜索结果详情。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动电话')
                self.start_phone()
            self.step(2, '点击屏幕底部联系人')
            self.open_tab('通讯录')
            self.step(3, '联系人页面，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(4, '点击搜索框')
            self.open_contact_search()
            self.step(5, '输入atest，点击第一条搜索记录，进入详情页面')
            self.search_contact('atest')
            self.step(6, '返回联系人界面')
            self.return_to_contacts()
            self.step(7, '联系人页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '返回电话主界面')
            self.return_phone_main()
            with self.capture_trace(iteration, 9):
                self.step(9, '滑动返回Home页')
                self.launcher()
