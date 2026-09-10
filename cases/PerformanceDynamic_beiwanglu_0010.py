from aw import SeaOfStarsAW
from cases.beiwanglu_common import BeiwangluCase


class PerformanceDynamic_beiwanglu_0010(BeiwangluCase):
    """Excel 7.0.2：备忘录新建待办事项。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动备忘录')
                self.start_notes()
            self.step(2, '点击右下角新建图标')
            self.new_note()
            self.step(3, '输入动态并点击保存')
            self.replace_note_text('动态')
            self.save_note()
            self.step(4, '返回备忘录首页')
            self.return_notes_list()
            self.step(5, '点击屏幕底部待办，切换到待办页')
            self.open_first_note()
            self.switch_to_checklist()
            self.step(6, '点击新建按钮，拉起小艺输入法')
            self.focus_new_checklist_item()
            self.step(7, '26键盘输入test，点击键盘上的回车按钮')
            self.enter_checklist_item('test')
            self.step(8, '点击保存按钮')
            self.save_note()
            self.step(9, '返回备忘录主界面')
            self.return_notes_list()
            with self.capture_trace(iteration, 10):
                self.step(10, '滑动返回Home页')
                self.launcher()


# 兼容 Excel 7.0 分工表中的大写拼法。
PerformanceDynamic_Beiwanglu_0010 = PerformanceDynamic_beiwanglu_0010
