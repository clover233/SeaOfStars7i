import time

from aw import SeaOfStarsAW
from cases.weibo_common import WeiboCase


class PerformanceDynamic_weibo_0020(WeiboCase):
    """微博推荐、关注、直播、超话与视频浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微博')
                self.start_weibo()
            self.step(2, '点击首页')
            self.tap_bottom_tab('微博')
            self.step(3, '点击推荐')
            self.select_home_channel('推荐')
            self.step(4, '推荐页面，上滑5次，下滑6次')
            self.browse(5, 6)
            self.step(5, '点击关注')
            self.select_home_channel('关注')
            self.step(6, '关注页面，上滑5次，下滑5次')
            self.browse(5, 5)
            self.step(7, '点击屏幕左上角第一个直播博主')
            self.open_first_live()
            self.step(8, '上滑5次、下滑5次，浏览直播页面')
            self.browse(5, 5)
            self.step(9, '返回关注界面')
            self.return_from_live()
            self.step(10, '长按底部视频tab按钮')
            self.long_press_video_tab()
            self.step(11, '点击超话')
            self.open_super_topic_after_long_press()
            self.step(12, '浏览超话页面，上滑3次，下滑3次')
            self.browse_super_topic_index()
            self.step(13, '点击第一条超话')
            self.open_first_super_topic()
            self.step(14, '上滑3次，下滑3次浏览超话内容')
            self.browse(3, 3)
            self.step(15, '返回超话界面')
            back = self._top_back()
            if back is not None:
                self.tap_node(back)
                time.sleep(3)
            self.step(16, '长按底部超话tab按钮')
            self.long_press_super_topic_tab()
            self.step(17, '点击视频')
            self.open_video_after_long_press()
            self.step(18, '点击首页，返回微博主界面')
            self.return_weibo_home()
            with self.capture_trace_5s(iteration, 19):
                self.step(19, '滑动返回Home页')
                self.launcher()
