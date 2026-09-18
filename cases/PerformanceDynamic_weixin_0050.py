from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0050(WeixinCase):
    """Excel 7.0.2：科技公众号资料、文章及官网入口浏览。"""

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
            self.step(4, '点击{}名片，进入资料页'.format(self.TECH_ACCOUNT))
            self.open_official_account(self.TECH_ACCOUNT)
            self.step(5, '浏览公众号/服务号资料页')
            self.browse(2, 2)
            self.step(6, '点击第一篇文章')
            self.open_first_official_article()
            self.step(7, '浏览文章页面')
            self.browse(3, 3)
            self.step(8, '返回{}资料页'.format(self.TECH_ACCOUNT))
            self.return_official_profile(self.TECH_ACCOUNT)
            self.return_contacts()
            self.tap('公众号', min_y=300, max_y=500, wait=3)
            self.step(9, '点击{}公众号名片'.format(self.HARMONY_ACCOUNT))
            self.open_official_account(self.HARMONY_ACCOUNT)
            self.open_official_chat()
            self.step(10, '点击屏幕底部HMOS后点击官网直达')
            self.tap('HMOS', min_y=760, wait=1)
            self.tap('官网直达', min_y=600, wait=5)
            self.step(11, '上滑2次，下滑2次浏览官网文章')
            self.browse(2, 2)
            self.step(12, '返回公众号界面')
            self.return_official_profile(self.HARMONY_ACCOUNT)
            self.step(13, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
