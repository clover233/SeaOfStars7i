from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0130(WeixinCase):
    """新版步骤：腾讯新闻、央视新闻及公众号信息流浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击通讯录')
            self.open_contacts()
            self.step(3, '点击公众号')
            self.tap('公众号', min_y=300, max_y=500, wait=3)
            self.step(4, '点击腾讯新闻的公众号名片')
            self.open_official_account(self.TENCENT_NEWS_ACCOUNT)
            self.step(5, '返回公众号界面')
            self.return_official_list()
            self.step(6, '点击央视新闻的公众号名片')
            self.open_official_account(self.CCTV_NEWS_ACCOUNT)
            self.open_official_chat()
            self.step(7, '点击屏幕底部文博日历查看详情')
            self.open_official_feature(('文博日历',), ('打卡笔记',))
            self.step(8, '浏览任意主题（如打卡笔记），上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(9, '返回央视新闻对话界面')
            self.edge_back(wait=4)
            self.step(10, '点击屏幕底部夜读查看详情')
            self.open_official_feature(('夜读',))
            self.step(11, '返回微信首页')
            self.return_weixin_home()
            self.step(12, '点击订阅号')
            self.open_subscription_feed()
            self.step(13, '点击腾讯新闻')
            self.open_subscription_account(self.TENCENT_NEWS_ACCOUNT)
            self.step(14, '腾讯新闻页面下滑3次')
            self.browse(3, 0)
            self.step(15, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
