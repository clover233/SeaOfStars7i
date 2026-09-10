from aw import SeaOfStarsAW
from cases.autonavi_common import AutonaviCase


class PerformanceDynamic_autonavi_0080(AutonaviCase):
    """Excel 7.0.2：恢复高德并退出后台导航。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '恢复后台导航')
                self.resume_navigation()
            self.step(2, '进入导航页面后退出后台导航返回首页')
            self.open_exit_navigation()
            self.confirm_exit_navigation()
            self.return_autonavi_home()
            with self.capture_trace(iteration, 3):
                self.step(3, '滑动返回Home页')
                self.launcher()
