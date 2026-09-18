from aw import SeaOfStarsAW
from cases.xhs_common import XhsCase


class PerformanceDynamic_xhs_0050(XhsCase):
    """小红书图片缩放和视频流浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动小红书')
                self.start_xhs()

            self.step(2, '点击右上角搜索')
            self.open_search()
            self.step(3, '在输入框输入“图片”')
            self.set_search_text('图片')
            self.step(4, '点击搜索')
            self.submit_search()
            self.step(5, '点击左上角第一条内容，并打开图片大图')
            self.open_first_search_result()
            self.open_note_image_viewer()
            self.step(6, '双指捏合放大图片')
            self.pinch_zoom_in()
            self.step(7, '双指捏合缩小图片')
            self.pinch_zoom_out()
            self.step(8, '重复放大、缩小两遍')
            self.repeat_pinch_cycle(2)
            self.step(9, '返回小红书主界面')
            self.return_home()
            self.step(10, '当前版本使用搜索结果的视频筛选替代视频tab')
            self.open_video_results()
            self.step(11, '点击第一条视频，浏览10秒')
            self.open_first_video_result()
            self.step(12, '视频流上滑3次，每次间隔5秒')
            self.browse_slow(3, 0)
            self.step(13, '视频流下滑3次，每次间隔5秒')
            self.browse_slow(0, 3)
            self.step(14, '返回首页推荐页')
            self.return_home()
            self.tap('发现', max_y=130, wait=3)

            with self.capture_trace_5s(iteration, 15):
                self.step(15, '滑动返回Home页')
                self.launcher()
