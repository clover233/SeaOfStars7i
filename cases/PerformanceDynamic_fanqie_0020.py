import time

from aw import SeaOfStarsAW
from cases.fanqie_common import FanqieCase


class PerformanceDynamic_fanqie_0020(FanqieCase):
    """Excel 7.0.2：浏览听书与完整榜单。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动番茄免费小说')
                self.start_fanqie()
            self.step(2, '主页浏览，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(3, '点击听书，进入听书页面')
            self.open_listen_page()
            self.step(4, '听书页浏览，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '点击推荐进入首页')
            self.tap('推荐', max_y=150, wait=3)
            self.step(6, '点击完本榜，进入完本榜页面')
            self.open_full_ranking()
            self.step(7, '左滑2次，右滑2次，浏览完本榜单')
            self.browse_ranking()
            self.step(8, '点击口碑榜，进入口碑榜页面')
            self.switch_ranking('口碑榜', '书友榜')
            self.step(9, '左滑2次，右滑2次，浏览口碑榜单')
            self.browse_ranking()
            self.step(10, '点击高分榜，进入高分榜页面')
            self.switch_ranking('高分榜', '书荒榜')
            self.step(11, '左滑2次，右滑2次，浏览高分榜单')
            self.browse_ranking()
            self.step(12, '返回番茄免费小说主界面')
            self.return_main()
            with self.capture_trace(iteration, 13):
                self.step(13, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
