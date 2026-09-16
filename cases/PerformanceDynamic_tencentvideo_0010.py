from aw import SeaOfStarsAW
from cases.tencentvideo_common import TencentVideoCase


class PerformanceDynamic_tencentvideo_0010(TencentVideoCase):
    """Excel 7.0.2：腾讯视频首页、播放和搜索浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动腾讯视频')
                self.start_tencentvideo()
            self.step(2, '首页浏览，上滑2次，下滑2次')
            self.browse(2, 2)
            self.step(3, '点击首页第一个推荐视频播放30s')
            self.open_first_recommended_video()
            self.step(4, '切换到全屏模式')
            self.enter_fullscreen()
            self.step(5, '退出全屏模式')
            self.exit_fullscreen()
            self.step(6, '浏览屏幕底部推荐视频，上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(7, '返回腾讯视频主界面')
            self.return_main()
            self.step(8, '点击搜索框')
            self.open_search()
            self.step(9, '输入斗破苍穹并搜索')
            self.search('斗破苍穹')
            self.step(10, '上滑3次，下滑3次浏览搜索结果')
            self.browse(3, 3)
            self.step(11, '点击影视，切换到影视界面')
            self.select_video_filter()
            self.step(12, '上滑1次，下滑1次浏览影视搜索结果')
            self.browse(1, 1)
            self.step(13, '返回腾讯视频主界面')
            self.return_main()
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
