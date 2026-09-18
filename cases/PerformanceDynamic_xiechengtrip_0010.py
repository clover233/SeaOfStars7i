from aw import SeaOfStarsAW
from cases.xiechengtrip_common import XiechengTripCase


class PerformanceDynamic_xiechengtrip_0010(XiechengTripCase):
    """携程民宿搜索、点评及设施浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动携程旅行')
                self.start_xiecheng()

            self.step(2, '向上抛滑1次，浏览首页')
            self.browse(1, 0)
            self.step(3, '向下抛滑2次，浏览首页')
            self.browse(0, 2)
            self.step(4, '点击民宿/客栈，进入民宿客栈页面')
            self.open_homestay()
            self.step(5, '向上抛滑2次，浏览民宿客栈页面')
            self.browse(2, 0)
            self.step(6, '向下抛滑3次，浏览民宿客栈页面')
            self.browse(0, 3)
            self.step(7, '点击查询，进入民宿查询结果页面')
            self.query_homestay()
            self.step(8, '输入“臻选民宿”并搜索')
            self.search_homestay('臻选民宿')
            self.step(9, '点击第一条民宿结果')
            self.open_first_homestay()
            self.step(10, '向上抛滑2次，浏览民宿详情')
            self.browse(2, 0)
            self.step(11, '点击评价，定位到房客点评')
            self.open_reviews()
            self.step(12, '点击动态显示的全部评论入口')
            self.open_all_reviews()
            self.step(13, '评论页上滑2次、下滑3次')
            self.browse(2, 3)
            self.step(14, '左侧滑动返回民宿详情页')
            self.edge_back()
            self.step(15, '点击全部设施，进入全部设施页')
            self.open_all_facilities()
            self.step(16, '点击右上角关闭全部设施弹窗')
            self.close_facilities()
            self.step(17, '向下抛滑3次，浏览民宿详情')
            self.browse(0, 3)
            self.step(18, '返回携程旅行主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 19):
                self.step(19, '滑动返回Home页')
                self.launcher()
