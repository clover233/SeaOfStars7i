from aw import SeaOfStarsAW
from cases.beiwanglu_common import BeiwangluCase


class PerformanceDynamic_beiwanglu_0020(BeiwangluCase):
    """Excel 7.0.2：备忘录浏览备忘录列表。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动备忘录')
                self.start_notes()
            self.step(2, '上滑2次，下滑2次，查看备忘录列表')
            self.browse(2, 2)
            self.step(3, '点击第一条备忘录查看内容')
            self.open_first_note()
            self.step(4, '返回备忘录主界面')
            self.return_notes_list()
            with self.capture_trace(iteration, 5):
                self.step(5, '滑动返回Home页')
                self.launcher()


# 兼容 Excel 7.0 分工表中的大写拼法。
PerformanceDynamic_Beiwanglu_0020 = PerformanceDynamic_beiwanglu_0020
