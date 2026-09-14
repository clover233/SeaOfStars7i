from aw import SeaOfStarsAW
from cases.mihome_common import MiHomeCase


class PerformanceDynamic_mihome_0010(MiHomeCase):
    """Excel 7.0.2：浏览米家产品、智能并进入添加设备。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动米家')
                self.start_mihome()
            self.step(2, '点击产品，切换到产品页')
            self.open_tab('产品')
            self.step(3, '产品页面上下滑动3次')
            self.browse(3, 3)
            self.step(4, '点击智能，切换到智能页')
            self.open_tab('智能')
            self.step(5, '智能页面上下滑动3次')
            self.browse(3, 3)
            self.step(6, '点击回家，切换到回家页')
            self.open_go_home()
            self.step(7, '点击米家，回到首页')
            self.return_home()
            self.step(8, '点击右上角加号，添加设备')
            self.open_add_device()
            self.step(9, '返回米家主界面')
            self.return_home()
            with self.capture_trace(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()
