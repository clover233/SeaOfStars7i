import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qqm_0010(Case):
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
    #     清空后台

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
            # step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            logging.info('启动QQ音乐')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '启动QQ音乐')
            SeaOfStarsAW.ut_device.click(0.38, 0.58)
            time.sleep(8)
            logging.info('点击我的')
            SeaOfStarsAW.ut_device(label='我的').click()
            time.sleep(2)
            logging.info('点击最近播放')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '浏览最近')
            SeaOfStarsAW.ut_device(label='最近播放').click()
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击本地')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '查看本地')
            SeaOfStarsAW.ut_device.click(0.38, 0.359)
            time.sleep(1)
            logging.info('返回')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('首页')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='首页').click()
            time.sleep(2)
            logging.info('点击搜索框')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '浏览搜索结果')
            SeaOfStarsAW.ut_device.click(0.335, 0.126)
            time.sleep(2)
            logging.info('输入红旗飘飘')
            SeaOfStarsAW.ut_device.send_keys('红旗飘飘')
            time.sleep(1)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('点击歌手')
            SeaOfStarsAW.ut_device.click(0.856, 0.123)
            time.sleep(2)
            logging.info('点击综合')
            SeaOfStarsAW.ut_device.click(0.079, 0.125)
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击第一个结果播放')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '播放、暂停、收藏音乐')
            SeaOfStarsAW.ut_device.click(0.246, 0.356)
            time.sleep(2)
            logging.info('点击查看播放详情')
            SeaOfStarsAW.ut_device.click(0.485, 0.31)
            time.sleep(2)
            logging.info('点击退出查看播放详情')
            SeaOfStarsAW.ut_device.click(0.485, 0.31)
            time.sleep(2)
            logging.info('点击暂停播放')
            SeaOfStarsAW.ut_device(label='暂停').click()
            time.sleep(2)
            logging.info('点击收藏')
            SeaOfStarsAW.ut_device(label='收藏').click()
            time.sleep(2)
            logging.info('点击取消收藏')
            SeaOfStarsAW.ut_device(label='已收藏').click()
            time.sleep(2)
            logging.info('左滑至歌词界面')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            logging.info('右滑返回')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            logging.info('隐藏正在播放界面')
            SeaOfStarsAW.ut_device(label='隐藏正在播放界面').click()
            time.sleep(2)
            logging.info('返回首页')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            logging.info('点击乐馆')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='乐馆').click()
            time.sleep(2)
            logging.info('上滑')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '榜单切换')
            logging.info('点击排行榜')
            SeaOfStarsAW.ut_device(label='排行榜').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击热歌榜')
            SeaOfStarsAW.ut_device(label='热歌榜').click()
            time.sleep(2)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击新歌榜')
            SeaOfStarsAW.ut_device(label='新歌榜').click()
            time.sleep(2)
            logging.info('点击分享')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '点击分享')
            SeaOfStarsAW.ut_device(label='分享').click()
            time.sleep(2)
            logging.info('点击音乐卡片')
            SeaOfStarsAW.ut_device(label='音乐卡片').click()
            time.sleep(2)
            logging.info('点击关闭')
            SeaOfStarsAW.ut_device(label='关闭').click()
            time.sleep(2)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')