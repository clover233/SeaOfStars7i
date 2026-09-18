from aw import SeaOfStarsAW
from cases.zhihu_common import ZhihuCase


class PerformanceDynamic_zhihu_0030(ZhihuCase):
    """Excel 7.0.2：知乎推荐、热榜、评论及壁纸搜索。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动知乎')
                self.start_zhihu()
            self.finish_zhihu_start()
            self.step(2, '点击屏幕顶部推荐')
            self.select_home_channel('home_page.recommend')
            self.step(3, '上滑2次、下滑3次浏览推荐')
            self.browse(2, 3)
            self.step(4, '点击屏幕顶部热榜')
            self.select_home_channel('home_page.hot')
            self.step(5, '上滑2次、下滑3次浏览热榜')
            self.browse(2, 3)
            self.step(6, '点击热榜第一条查看详情')
            self.open_first_hot_topic()
            self.step(7, '上滑2次、下滑3次浏览详情')
            self.browse(2, 3)
            self.step(8, '点击第一条回答查看具体信息')
            self.open_first_answer()
            self.step(9, '上滑2次、下滑3次浏览文章')
            self.browse(2, 3)
            self.step(10, '点击右下角评论按钮')
            self.open_comments()
            self.step(11, '上滑2次、下滑3次浏览评论')
            self.browse(2, 3)
            self.step(12, '返回推荐页')
            self.return_recommend()
            self.step(13, '搜索一组桌面壁纸')
            self.search('一组桌面壁纸')
            self.step(14, '点击搜索的第一条结果')
            self.open_first_wallpaper_result()
            self.step(15, '点击第一张图片')
            self.open_first_wallpaper()
            self.step(16, '左滑2次、右滑2次浏览图片')
            self.browse_wallpapers()
            self.step(17, '返回知乎首页')
            self.return_zhihu_home()
            self.step(18, '点击底部看山（替代已下线的发现 tab）')
            self.open_discover_equivalent()
            self.step(19, '返回知乎主界面')
            self.return_zhihu_home()
            with self.capture_trace_5s(iteration, 20):
                self.step(20, '滑动返回Home页')
                self.launcher()
