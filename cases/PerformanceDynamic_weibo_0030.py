from aw import SeaOfStarsAW
from cases.weibo_common import WeiboCase


class PerformanceDynamic_weibo_0030(WeiboCase):
    """微博热搜、正文、赞、评论与转发面板。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微博')
                self.start_weibo()
            self.step(2, '点击屏幕底部发现')
            self.step(3, '点击更多热搜进入热搜界面')
            self.open_more_hot_searches()
            self.step(4, '热搜界面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(5, '点击微博热搜第一条')
            self.open_first_hot_search()
            self.step(6, '点击第一条博文，查看正文')
            self.open_first_post()
            self.step(7, '正文页面上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(8, '点击右下角赞')
            self.toggle_like()
            self.step(9, '再次点击赞，取消赞')
            self.toggle_like()
            self.step(10, '点击评论，输入评论')
            self.comment_without_sending('评论')
            self.step(11, '点击取消，返回博文正文界面')
            self.cancel_comment()
            self.step(12, '点击转发微博')
            self.open_repost()
            self.step(13, '点击取消')
            self.cancel_repost()
            self.step(14, '返回微博主界面')
            self.return_weibo_home()
            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
