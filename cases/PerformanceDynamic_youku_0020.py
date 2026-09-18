from aw import SeaOfStarsAW
from cases.youku_common import YoukuCase


class PerformanceDynamic_youku_0020(YoukuCase):
    """Excel 7.0.2：优酷浏览动漫、电影及搜索播放。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动优酷')
                self.start_youku()
            self.finish_youku_start()
            self.step(2, '首页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(3, '点击动漫 tab 页')
            self.select_channel('动漫')
            self.step(4, '动漫页上滑3次、下滑3次')
            self.browse(3, 3)
            self.step(5, '点击电影 tab 页')
            self.select_channel('电影')
            self.step(6, '电影页上滑3次、下滑3次')
            self.browse(3, 3)
            self.step(7, '返回推荐页并打开搜索页')
            self.return_youku_home()
            self.open_search()
            self.step(8, '输入大话天仙')
            self.input_search('大话天仙')
            self.step(9, '搜索视频大话天仙，重复搜索2次')
            self.submit_search()
            self.repeat_search('大话天仙')
            self.step(10, '点击播放大话天仙，观看30秒')
            self.play_dahuatextian(seconds=30)
            self.step(11, '视频播放页上滑5次、下滑5次')
            self.browse(5, 5)
            self.step(12, '返回优酷主界面')
            self.return_youku_home()
            with self.capture_trace_5s(iteration, 13):
                self.step(13, '上滑返回桌面')
                self.launcher()
