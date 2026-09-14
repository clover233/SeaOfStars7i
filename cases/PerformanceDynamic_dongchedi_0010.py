from aw import SeaOfStarsAW
from cases.dongchedi_common import DongchediCase


class PerformanceDynamic_dongchedi_0010(DongchediCase):
    """Excel 7.0.2：懂车帝推荐、搜索、图片与热榜浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动懂车帝')
                self.start_dongchedi()
            self.step(2, '推荐页上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(3, '点击关注')
            self.open_following()
            self.step(4, '关注页上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(5, '点击推荐，返回推荐页面')
            self.return_recommendation()
            self.step(6, '点击搜索框')
            self.open_search()
            self.step(7, '输入奥迪A8，点击搜索')
            self.search('奥迪A8')
            self.step(8, '点击第一个搜索结果')
            self.open_first_search_result('奥迪A8')
            self.step(9, '点击图片')
            self.open_gallery()
            self.step(10, '点击查看第一张图片')
            self.open_first_picture()
            self.step(11, '图片页左滑3次，右滑3次')
            self.browse_pictures(3, 3)
            self.step(12, '返回图片界面')
            self.return_to_gallery()
            self.step(13, '返回搜索界面')
            self.return_search_landing()
            self.step(14, '点击热榜下第一条新闻')
            self.open_first_hot_news()
            self.step(15, '新闻页上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(16, '返回懂车帝主界面')
            self.return_home()
            with self.capture_trace(iteration, 17):
                self.step(17, '滑动返回Home页')
                self.launcher()
