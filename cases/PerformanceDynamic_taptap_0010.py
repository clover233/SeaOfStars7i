from aw import SeaOfStarsAW
from cases.taptap_common import TapTapCase


class PerformanceDynamic_taptap_0010(TapTapCase):
    """Excel 7.0.2：TapTap 搜索、评价、榜单、社区和个人页浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动TapTap')
                self.start_taptap()
            self.step(2, '找游戏页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(3, '点击搜索框，搜索王者荣耀')
            self.search_game('王者荣耀')
            self.step(4, '点击第一条搜索结果')
            self.open_first_result('王者荣耀')
            self.step(5, '点击评价')
            self.open_reviews()
            self.step(6, '评价页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(7, '侧滑返回找游戏页')
            self.return_find_games()
            self.step(8, '点击排行榜')
            self.open_tab('排行榜')
            self.step(9, '点击社区')
            self.open_tab('社区')
            self.step(10, '社区详情上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(11, '点击我的游戏')
            self.open_my_games()
            self.step(12, '点击个人主页')
            self.open_personal_profile()
            self.step(13, '侧滑返回TapTap首页')
            self.return_find_games()
            with self.capture_trace(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
