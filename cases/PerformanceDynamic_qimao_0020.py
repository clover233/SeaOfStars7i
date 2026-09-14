import time

from aw import SeaOfStarsAW
from cases.qimao_common import QimaoCase


class PerformanceDynamic_qimao_0020(QimaoCase):
    """Excel 7.0.2：首页、小说、短剧、分类与搜索综合浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace(iteration, 1):
                self.step(1, '启动七猫免费小说')
                self.start_qimao()
            self.step(2, '主页浏览，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(3, '点击小说，进入小说页面')
            self.tap('小说', max_y=170, wait=4)
            self.step(4, '小说页面滑动浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(5, '点击短剧，进入短剧页面')
            self.tap('短剧', max_y=170, wait=4)
            self.step(6, '短剧页面滑动浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(7, '点击分类，进入分类页面')
            self.tap('分类', min_y=760, wait=4)
            self.step(8, '点击现代言情，进入现代言情页面')
            self.tap('现代言情', min_y=120, max_y=760, wait=4)
            self.step(9, '现代言情页面滑动浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(10, '点击最高评分')
            self.tap('最高评分', min_y=250, max_y=600, wait=4)
            self.step(11, '现代言情页面滑动浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(12, '返回七猫免费小说主界面')
            self.return_book_city()
            self.step(13, '点击搜索框，进入搜索界面')
            self.open_search()
            self.step(14, '输入长生进行搜索，进入搜索结果页面')
            self.search_book('长生')
            self.step(15, '返回七猫免费小说主界面')
            self.return_book_city()
            with self.capture_trace(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
                time.sleep(5)
