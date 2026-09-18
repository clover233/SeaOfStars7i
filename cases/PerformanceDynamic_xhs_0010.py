from aw import SeaOfStarsAW
from cases.xhs_common import XhsCase


class PerformanceDynamic_xhs_0010(XhsCase):
    """小红书收藏、设置、消息和照片浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动小红书')
                self.start_xhs()

            self.step(2, '点击我，进入个人页面')
            self.open_profile()
            self.step(3, '点击收藏，并打开第一条收藏图片内容')
            self.open_collection()
            self.open_first_collection_note()
            self.step(4, '点击左下角点赞按钮')
            self.toggle_like()
            self.step(5, '浏览图片内容，向左滑动3次')
            self.horizontal_browse(3, 0)
            self.step(6, '返回个人页面')
            self.return_profile()
            self.step(7, '点击设置图标，进入设置界面')
            self.open_settings()
            self.step(8, '返回小红书主界面')
            self.return_from_settings_to_home()
            self.step(9, '首页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(10, '点击消息，进入消息页面')
            self.tap_bottom_tab('消息')
            self.step(11, '点击我，进入个人页面')
            self.open_profile()
            self.step(12, '再次点击消息，进入消息页面')
            self.tap_bottom_tab('消息')
            self.step(13, '点击首页')
            self.tap_bottom_tab('首页')
            self.step(14, '点击加号按钮，进入照片选择页面')
            self.open_photo_picker()
            self.step(15, '照片页面上滑3次、下滑3次')
            self.browse(3, 3)
            self.step(16, '点击第一张照片查看大图')
            self.open_first_photo_preview()
            self.step(17, '大图左滑3次、右滑3次')
            self.horizontal_browse(3, 3)
            self.step(18, '返回小红书主界面')
            self.return_home()

            with self.capture_trace_5s(iteration, 19):
                self.step(19, '滑动返回Home页')
                self.launcher()
