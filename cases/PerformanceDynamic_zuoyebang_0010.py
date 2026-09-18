from aw import SeaOfStarsAW
from cases.zuoyebang_common import ZuoyebangCase


class PerformanceDynamic_zuoyebang_0010(ZuoyebangCase):
    """作业帮首页、拍照、练习、VIP 和学习好物浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动作业帮')
                self.start_zuoyebang()

            self.step(2, '首页上滑1次、下滑1次')
            self.browse(1, 1)
            self.step(3, '点击搜索答疑')
            self.open_search_answer()
            self.step(4, '点击拍照')
            self.take_photo()
            self.step(5, '点击左上角两次关闭，返回作业帮首页')
            self.close_camera_to_home()
            self.step(6, '点击作业批改')
            self.open_homework_correction()
            self.step(7, '返回作业帮首页')
            self.close_camera_once()
            self.step(8, '点击练习（同步学练）tab')
            self.open_practice()
            self.step(9, '练习页面上滑2次、下滑2次')
            self.browse(2, 2)
            self.step(10, '点击VIP')
            self.open_vip()
            self.step(11, 'VIP页面上滑2次、下滑2次')
            self.browse(2, 2)
            self.step(12, '点击学习好物')
            self.open_learning_goods()
            self.step(13, '学习好物页面上滑2次、下滑2次')
            self.browse(2, 2)
            self.step(14, '返回作业帮主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
