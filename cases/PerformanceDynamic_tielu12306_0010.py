from aw import SeaOfStarsAW
from cases.tielu12306_common import Tielu12306Case


class PerformanceDynamic_tielu12306_0010(Tielu12306Case):
    """Excel 7.0.2：铁路12306车票结果和排序浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动铁路12306')
                self.start_tielu12306()
            self.step(2, '向上抛滑1次，浏览首页')
            self.browse(1, 0)
            self.step(3, '向下抛滑2次，浏览首页')
            self.browse(0, 2)
            self.step(4, '点击首页的查询车票')
            self.open_ticket_results()
            self.step(5, '向上抛滑2次，浏览信息')
            self.browse(2, 0)
            self.step(6, '向下抛滑3次，浏览信息')
            self.browse(0, 3)
            self.step(7, '点击耗时最短')
            self.select_result_sort('耗时最短')
            self.step(8, '点击发时最早')
            self.select_result_sort('出发最早', '出发从早到晚排序',
                                    '发时最早', '最早发车')
            self.step(9, '点击价格最低')
            self.select_result_sort('价格最低')
            self.step(10, '返回铁路12306主界面')
            self.return_home()
            with self.capture_trace_5s(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
