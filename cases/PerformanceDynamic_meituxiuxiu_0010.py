import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_meituxiuxiu_0010(Case):
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
            step = 0
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、打开美图秀秀，停留3s
            logging.info('启动美图秀秀，等待3s')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '启动美图秀秀')
            SeaOfStarsAW.ut_device.session().app_activate('com.meitu.mtxx')
            time.sleep(3)

            # 2、点击导入图片
            logging.info('点击导入图片')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '点击导入图片')
            time.sleep(5) # 跳过广告
            SeaOfStarsAW.ut_device.click(0.263, 0.329, 0.50)
            time.sleep(1)


            # 3、选择第一张图片，点击滤镜
            logging.info('选择第一张图片，点击滤镜')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '选择第一张图片，点击滤镜')
            SeaOfStarsAW.ut_device.click(0.117, 0.237, 0.50)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.699, 0.901, 0.50)
            time.sleep(1)

            # 4、选中从左往右第一种滤镜格式，并确认
            logging.info('选中从左往右第一种滤镜格式，并确认')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '选中从左往右第一种滤镜格式，并确认')
            SeaOfStarsAW.ut_device.click(0.945, 0.939, 0.50)
            time.sleep(1)

            # 5、点击调色，并设置亮度为100 %，点击确认
            logging.info('点击调色，并设置亮度为100 %，点击确认')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '点击调色，并设置亮度为100 %，点击确认')
            SeaOfStarsAW.ut_device.click(0.55, 0.901, 0.50)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.842, 0.782, 0.50)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.948, 0.939, 0.50)
            time.sleep(1)

            # 6、点击保存
            logging.info('点击保存')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '点击保存')
            SeaOfStarsAW.ut_device.click(0.822, 0.1, 0.50)
            time.sleep(1)

            # 7、点击“再修一张”
            logging.info('点击“再修一张”')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '点击“再修一张”')
            SeaOfStarsAW.ut_device.click(0.65, 0.164, 0.50)
            time.sleep(1)

            # 8、左滑返回到“选择相册”界面。 直接回主界面了
            logging.info('左滑返回到“选择相册”界面')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '左滑返回到“选择相册”界面')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 9、返回“导入图片界面”
            logging.info('返回“导入图片界面”')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '返回“导入图片界面”')
            SeaOfStarsAW.ut_device.click(0.255, 0.32, 0.50)
            time.sleep(1)

            # 10、上滑返回桌面
            logging.info('上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('美图秀秀', '上滑返回桌面')
            SeaOfStarsAW.swipe_to_launcher()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate('com.meitu.mtxx')

        logging.info('用例执行结束')