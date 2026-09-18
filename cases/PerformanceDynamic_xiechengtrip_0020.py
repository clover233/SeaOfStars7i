from aw import SeaOfStarsAW
from cases.xiechengtrip_common import XiechengTripCase


class PerformanceDynamic_xiechengtrip_0020(XiechengTripCase):
    """携程机票和火车票结果浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动携程旅行')
                self.start_xiecheng()

            self.step(2, '点击机票，并关闭可选弹窗')
            self.open_flight()
            self.step(3, '点击查询，进入机票搜索结果')
            self.query_flight()
            self.step(4, '机票结果页上滑3次、下滑4次')
            self.browse(3, 4)
            self.step(5, '查看第一条机票搜索结果详情')
            self.open_first_flight()
            self.step(6, '返回携程旅行首页')
            self.return_home()
            self.step(7, '点击火车票')
            self.open_train()
            self.step(8, '点击查询，进入火车票搜索结果')
            self.query_train()
            self.step(9, '火车票结果页上滑3次、下滑4次')
            self.browse(3, 4)
            self.step(10, '查看第一条火车票搜索结果详情')
            self.open_first_train()
            self.step(11, '点击预订，进入订单填写页但不提交')
            self.book_first_train()
            self.step(12, '返回携程旅行主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 13):
                self.step(13, '滑动返回Home页')
                self.launcher()
