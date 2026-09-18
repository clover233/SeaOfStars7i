from aw import SeaOfStarsAW
from cases.weipinhui_common import WeipinhuiCase


class PerformanceDynamic_weipinhui_0030(WeipinhuiCase):
    """唯品会推荐、运动与奥莱等价频道浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动唯品会')
                self.start_weipinhui()
            self.step(2, '向上抛滑3次，浏览推荐页面')
            self.browse(3, 0)
            self.step(3, '点击运动，进入运动页面')
            self.open_sport()
            self.step(4, '向上抛滑3次，浏览运动页面')
            self.browse(3, 0)
            self.step(5, '进入唯品奥莱页面（新版使用天天低价等价入口）')
            self.open_outlet_equivalent()
            self.step(6, '上滑2次、下滑2次，浏览奥莱等价页面')
            self.browse(2, 2)
            self.step(7, '返回唯品会主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 8):
                self.step(8, '滑动返回Home页')
                self.launcher()
