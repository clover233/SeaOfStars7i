import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_bilibili_0030(Case):
    all_app_package_list = ['']
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        logging.info("用例开始执行")
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(2)
        for test_time in range(0, self.TEST_TIME):
            step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 启动哔哩哔哩
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('tv.danmaku.bilianime')

            # 点击热门
            logging.info('点击热门')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击热门')
            SeaOfStarsAW.ut_device.click(0.408, 0.143, 0.5)
            time.sleep(1)

            # 上滑5次浏览热门，间隔1s
            logging.info('上滑5次浏览热门')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '上滑5次浏览热门')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 下滑5次浏览热门，间隔1s
            logging.info('下滑5次浏览热门')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '下滑5次浏览热门')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)
            time.sleep(2)

            # 点击某一个视频播
            logging.info('点击某一个视频播')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击某一个视频播')
            SeaOfStarsAW.ut_device.click(0.479, 0.73, 0.3)
            time.sleep(1)

            # 点击屏幕调出菜单键，点击全屏按钮
            # 竖屏视频可能会导致切全屏失败 改 0.474, 0.322
            logging.info('点击屏幕调出菜单键，点击全屏按钮')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击屏幕调出菜单键，点击全屏按钮')
            SeaOfStarsAW.ut_device.double_tap(0.841, 0.203)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.942, 0.302, 0.5)
            time.sleep(1)

            # 观看10秒视频
            logging.info('观看10秒视频')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '观看10秒视频')
            time.sleep(10)

            # 双击屏幕继续观看5秒视频
            logging.info('双击屏幕继续观看5秒视频')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '双击屏幕继续观看5秒视频')
            SeaOfStarsAW.ut_device.double_tap(0.478, 0.478)
            time.sleep(5)

            # 侧滑退出全屏
            # 侧滑无法退出全屏
            logging.info('侧滑退出全屏')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '侧滑退出全屏')
            SeaOfStarsAW.ut_device.click(0.494, 0.482, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.1, 0.108, 0.2)
            time.sleep(1)

            # 点击评论
            logging.info('点击评论')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击评论')
            SeaOfStarsAW.ut_device.click(0.347, 0.42, 0.5)
            time.sleep(1)

            # 上滑5次浏览评论，间隔1s
            logging.info('上滑5次浏览评论')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '上滑5次浏览评论')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 下滑5次浏览评论，间隔1s
            logging.info('下滑5次浏览评论')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '下滑5次浏览评论')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 侧滑返回首页
            logging.info('返回哔哩哔哩首页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回哔哩哔哩首页')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
                time.sleep(1)

            # 返回桌面
            logging.info('返回桌面')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('tv.danmaku.bilianime')
            time.sleep(1)

        logging.info('用例执行结束')