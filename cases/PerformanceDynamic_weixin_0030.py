from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0030(WeixinCase):
    """Excel 7.0.2：通讯录好友资料、朋友圈图片及推荐。"""

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
            self.step(3, '通讯录页面，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(4, '进入好友{}的详情界面'.format(self.CONTACT_NAME))
            self.open_contact(self.CONTACT_NAME)
            self.step(5, '点击头像，并返回')
            self.view_contact_avatar()
            self.step(6, '点击好友的朋友圈')
            self.open_contact_moments_picture()
            self.step(7, '浏览图片，横向滑动6次')
            self.horizontal_browse(0, 6)
            self.step(8, '返回好友{}的详情界面'.format(self.CONTACT_NAME))
            self.return_contact_profile(self.CONTACT_NAME)
            self.step(9, '把她推荐给好友')
            self.recommend_contact(self.RECOMMEND_RECIPIENT)
            self.step(10, '返回微信主界面')
            self.return_weixin_home()
            self.step(11, '点击右上角+号')
            self.tap('快捷操作', max_y=120, wait=1)
            self.step(12, '点击扫一扫')
            self.tap('扫一扫', min_y=150, max_y=320, wait=3)
            self.step(13, '点击相册')
            self.tap('相册', min_y=600, wait=3)
            self.step(14, '选择一张图片')
            self.choose_first_photo()
            self.step(15, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 16):
                self.step(16, '滑动返回Home页')
                self.launcher()
