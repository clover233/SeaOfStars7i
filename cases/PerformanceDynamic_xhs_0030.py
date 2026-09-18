from aw import SeaOfStarsAW
from cases.xhs_common import XhsCase


class PerformanceDynamic_xhs_0030(XhsCase):
    """小红书“穿搭图片”和热搜浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动小红书')
                self.start_xhs()

            self.step(2, '点击右上角搜索')
            self.open_search()
            self.step(3, '搜索“穿搭图片”并返回搜索页，重复3次')
            self.repeat_search_and_return('穿搭图片', 3)
            self.step(4, '再次搜索“穿搭图片”')
            self.search_keyword('穿搭图片')
            self.step(5, '点击左上角第一条搜索结果')
            self.open_first_search_result()
            self.step(6, '笔记详情上滑1次、下滑1次')
            self.browse(1, 1)
            self.step(7, '点击图片看大图，左滑3次、右滑3次')
            self.open_note_image_viewer()
            self.horizontal_browse(3, 3)
            self.step(8, '返回搜索结果页面')
            self.edge_back()
            self.step(9, '搜索结果上滑3次、下滑3次，重复2次')
            for _ in range(2):
                self.browse(3, 3)
            self.step(10, '返回搜索页面')
            self.edge_back(wait=4)
            self.step(11, '点击搜索发现区域的第一条热搜')
            self.open_first_hot_search()
            self.step(12, '热搜页面上滑3次、下滑3次，重复2次')
            for _ in range(2):
                self.browse(3, 3)
            self.step(13, '返回小红书主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
