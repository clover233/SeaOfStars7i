import logging
import time
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hongguomianfeiduanju_0020(Case):
    all_app_package_list = ['com.phoenix.video']
    TEST_TIME = 1
    # Excel 未指定长按时长，默认保持倍速播放 3 秒。
    SPEED_PLAY_SECONDS = 3

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                raise RuntimeError('未安装测试应用：{}'.format(per_app))
        return True

    def _log_step(self, description):
        logging.info(description)
        SeaOfStarsAW.trace_thread.add_log('红果免费短剧', description)

    def _click(self, label, x, y):
        element = SeaOfStarsAW.ut_device(label=label)
        if element.exists:
            element.click()
        else:
            logging.warning('未找到文字控件“%s”，使用待真机校准的坐标：%s',
                            label, (x, y))
            SeaOfStarsAW.ut_device.click(x, y)
        time.sleep(2)

    def _swipe_back(self):
        SeaOfStarsAW.ut_device.swipe(0.01, 0.5, 0.95, 0.5, duration=0.5)
        time.sleep(2)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """推荐视频浏览、评论、追剧、搜索并横竖屏播放（Excel 第 7 行）。"""
        logging.info('用例开始执行')
        device = SeaOfStarsAW.ut_device
        if device.locked():
            device.unlock()
            time.sleep(2)

        for test_time in range(self.TEST_TIME):
            device.orientation = 'PORTRAIT'
            SeaOfStarsAW.start_trace(
                self.trace_dir_path,
                self.__class__.__name__,
                'step_' + str(test_time),
                self.screenshot_dir_path,
            )
            restore_portrait = False
            try:
                self._log_step('1、启动红果免费短剧')
                device.app_activate('com.phoenix.video')
                time.sleep(3)

                self._log_step('2、长按首页推荐视频倍速播放')
                device.tap_hold(0.5, 0.45, duration=self.SPEED_PLAY_SECONDS)
                time.sleep(1)

                self._log_step('3、点击评论按钮')
                self._click('评论', 0.92, 0.60)

                self._log_step('4、上滑3次，浏览评论')
                for _ in range(3):
                    # 手势限于底部评论面板，避免滑动背后的视频。
                    device.swipe(0.5, 0.85, 0.5, 0.55, duration=0.5)
                    time.sleep(1)

                self._log_step('5、下滑3次，浏览评论')
                for _ in range(3):
                    device.swipe(0.5, 0.55, 0.5, 0.85, duration=0.5)
                    time.sleep(1)

                self._log_step('6、侧滑退出评论')
                device.swipe(0.01, 0.7, 0.95, 0.7, duration=0.5)
                time.sleep(2)

                self._log_step('7、点击追剧')
                # 已追剧时保持该状态，避免重复运行将其取消。
                if device(label='已追剧').exists:
                    logging.info('当前视频已追剧，保持追剧状态')
                else:
                    self._click('追剧', 0.92, 0.72)

                self._log_step('8、点击剧场')
                self._click('剧场', 0.3, 0.95)

                self._log_step('9、点击右上角搜索')
                self._click('搜索', 0.92, 0.08)

                self._log_step('10、搜索仙帝')
                device().set_text('仙帝')
                time.sleep(1)
                self._click('搜索', 0.90, 0.08)

                self._log_step('11、上滑3次，浏览搜索结果')
                for _ in range(3):
                    device.swipe_up()
                    time.sleep(1)

                self._log_step('12、下滑3次，浏览搜索结果')
                for _ in range(3):
                    device.swipe_down()
                    time.sleep(1)

                self._log_step('13、点击进入第一条搜索结果')
                device.click(0.5, 0.30)
                time.sleep(2)

                self._log_step('14、竖屏观看视频10s')
                if device.orientation != 'PORTRAIT':
                    raise RuntimeError('播放器未处于竖屏，请检查第一条搜索结果是否已打开')
                time.sleep(10)

                self._log_step('15、切换至横屏观看视频20s')
                restore_portrait = True
                device.orientation = 'LANDSCAPE'
                time.sleep(2)
                if device.orientation != 'LANDSCAPE':
                    raise RuntimeError('未切换到横屏，请检查播放器横屏入口及屏幕旋转设置')
                time.sleep(20)

                self._log_step('16、返回剧场界面')
                device.orientation = 'PORTRAIT'
                time.sleep(2)
                restore_portrait = False
                # 视频、搜索结果、搜索输入页可能分别占用一层返回栈。
                for _ in range(3):
                    if device(label='剧场').exists:
                        break
                    self._swipe_back()
                if not device(label='剧场').exists:
                    raise RuntimeError('返回后未找到剧场入口，请检查播放器/搜索页面返回层级')
                device(label='剧场').click()
                time.sleep(2)

                self._log_step('17、点击首页')
                self._click('首页', 0.1, 0.95)

                self._log_step('18、滑动返回Home页')
                SeaOfStarsAW.swipe_to_launcher()
                time.sleep(2)
            finally:
                try:
                    if restore_portrait:
                        device.orientation = 'PORTRAIT'
                finally:
                    SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
