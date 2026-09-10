from aw import SeaOfStarsAW
from cases.baidu_common import BaiduCase


class PerformanceDynamic_baidu_0010(BaiduCase):
    """Excel 7.0.2：百度浏览器浏览搜索结果。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动百度浏览器')
                self.start_baidu()
            self.step(2, '点击底部文心一言')
            self.open_wenxin()
            self.step(3, '输入西安三天旅行攻略进行问答')
            self.ask_wenxin('西安三天旅行攻略')
            self.step(4, '返回百度主界面')
            self.return_baidu_home()
            self.step(5, '点击搜索框，拉起输入法')
            self.tap('SearchBox_test', fallback=(0.35, 0.09), wait=1)
            self.step(6, '输入西安百度百科点击搜索')
            self.enter_text('西安百度百科', clear=True)
            self.tap('Search', 'sug_search_button', fallback=(0.87, 0.895), wait=6)
            self.step(7, '浏览搜索结果，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '点击第一个搜索结果查看详情')
            self.open_first_baike_result()
            self.step(9, '上滑5次，下滑5次，查看搜索结果')
            self.browse(5, 5)
            self.step(10, '返回百度主界面')
            self.return_baidu_home()
            with self.capture_trace(iteration, 11):
                self.step(11, '滑动返回Home页')
                self.launcher()
