from aw import SeaOfStarsAW
from cases.wpsoffice_common import WpsOfficeCase


class PerformanceDynamic_wpsoffice_0010(WpsOfficeCase):
    """WPS 首页、云盘、设置、会员页和欢迎文档浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动WPS')
                self.start_wps()
            self.step(2, '首页左右滑动各5次')
            self.browse_horizontal(5, 5)
            self.step(3, '点击云盘后点击首页，重复5次')
            self.switch_cloud_home(5)
            self.step(4, '点击我')
            self.open_my()
            self.step(5, '点击设置')
            self.open_settings()
            self.step(6, '返回我的页面')
            self.back_to_my()
            self.step(7, '点击超级会员，进入支付界面')
            self.open_super_member()
            self.step(8, '返回我的页面')
            self.back_from_member()
            self.step(9, '点击首页')
            self.return_home()
            self.step(10, '点击欢迎使用WPS云文档')
            self.open_welcome_document()
            self.step(11, '上下滑动5次浏览文档页')
            self.browse_document(5, 5)
            self.step(12, '返回WPS主界面')
            self.back_from_document()
            self.return_home()
            with self.capture_trace_5s(iteration, 13):
                self.step(13, '滑动返回Home页')
                self.launcher()
