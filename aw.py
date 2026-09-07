import json
import logging
import os
import platform
import re
import shlex
import shutil
import subprocess
import openpyxl
import time
from functools import wraps
from threading import Timer
from enum import Enum
from enum import unique
import wda
from TraceTool.iTrace import iTraceThread


class SeaOfStarsAW:
    ut_device = None
    trace_thread = None
    error_screenshot_path = ''
    APP_INFO_DICT = {
        "com.meituan.imeituan":{"cn_name":"美团"},
        "com.xunmeng.pinduoduo": {"cn_name": "拼多多"},
        "com.alipay.iphoneclient": {"cn_name": "支付宝"},
        "com.taobao.taobao4iphone": {"cn_name": "淘宝"},
        "com.ss.android.ugc.aweme": {"cn_name": "抖音"},
        "com.autonavi.amap": {"cn_name": "高德地图"},
        "com.tencent.mtt": {"cn_name": "QQ浏览器"},
        "com.tencent.xin": {"cn_name": "微信"},
        "com.kugou.android": {"cn_name": "酷狗音乐"},
        "com.xingin.discover": {"cn_name": "小红书"},
        "com.youku.YouKu": {"cn_name": "优酷"},
        "com.qiyi.iphone": {"cn_name": "爱奇艺"},
        "com.tencent.mqq":{"cn_name": "QQ"},
        "com.tencent.smoba": {"cn_name": "王者荣耀"},
        "com.tencent.tmgp.pubgmhd": {"cn_name": "和平精英"},
        'com.happyelements.1OSAnimal': {"cn_name": "开心消消乐®"},
        'tv.danmaku.bilianime': {"cn_name": "哔哩哔哩"},
        'com.dragon.read': {"cn_name": "番茄小说"},
        'com.360buy.jdmobile': {"cn_name": "京东"},
        'com.netease.cloudmusic': {"cn_name": "网易云音乐"},
        'com.ss.iphone.article.News': {"cn_name": "今日头条"},
        'com.sina.weibo': {"cn_name": "微博"},
        'com.baidu.BaiduMobile': {"cn_name": "百度"},
        'com.tencent.live4iphone': {"cn_name": "腾讯视频"},
        'com.jiangjia.gif': {"cn_name": "快手"},
        'com.hunantv.imgotv':{"cn_name": "芒果TV"},
    }

    @staticmethod
    def return_launcher():
        """
        通过 'swipe' 命令 返回主桌面
        :return: None
        """
        SeaOfStarsAW.ut_device.swipe(0.504, 0.980, 0.340, 0.980, duration=0.02)
        time.sleep(2)
        SeaOfStarsAW.ut_device.swipe(0.504, 0.980, 0.340, 0.980, duration=0.02)
        time.sleep(2)

    @staticmethod
    def find_app_from_launcher(app_chinese_name, time_out=60):
        """
        在launcher的应用程序抽屉找到app图标，注意：需要系统语言为中文，app需要全部放在主桌面
        :param app_chinese_name:  app在launcher抽屉上的中文名全名
        :param time_out: 超时时间限制
        :return: 图标中心点坐标

        Notice:接口暂不可用，待调试
        """
        # 回到桌面主页
        # print(SeaOfStarsAW.ut_device(label=app_chinese_name).exists)
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.return_launcher()
        # logging.info("桌面启动{}应用".format(app_chinese_name))
        # 查找app坐标
        time_start = time.time()
        # while not SeaOfStarsAW.ut_device(label=app_chinese_name).exists and (time.time() - time_start) < time_out:
        #     SeaOfStarsAW.ut_device.swipe_right()
        #     time.sleep(1)
        if SeaOfStarsAW.ut_device(label=app_chinese_name).exists:
            return SeaOfStarsAW.ut_device(label=app_chinese_name).bounds.center

        elif SeaOfStarsAW.ut_device(name=app_chinese_name).exists:
            return SeaOfStarsAW.ut_device(name=app_chinese_name).bounds.center
        else:
            raise AssertionError("未找到app")
            return False

    @staticmethod
    def click_pos_from_launcher(pos, sleep_time=15):
        """
        点击坐标，默认等待15秒，用于应用启动
        :param pos: turpe，如(100,100)
        :return: None

        Notice:接口暂不可用，待调试
        """
        if len(pos) > 1:
            logging.info("点击坐标:{},{}".format(pos[0], pos[1]))
            # while pos[0]==pos[1]==0:
            #     SeaOfStarsAW.ut_device.swipe_right()
            #     pos=


            SeaOfStarsAW.ut_device.click(pos[0], pos[1])
            time.sleep(sleep_time)
        else:
            logging.info("pos为{}".format(pos))
            raise AssertionError("坐标有误")

    @staticmethod
    def function_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info("{0:=^40}".format(" " + func.__name__ + "开始执行"))
            res = func(*args, **kwargs)
            logging.info("{0:=^40}".format(" " + func.__name__ + "执行结束"))
            return res

        return wrapper

    @staticmethod
    def init_device(result_dir_path=None, serial_no=None):
        device = wda.Client('http://localhost:8100')
        # wda.DEBUG = True

        SeaOfStarsAW.ut_device = device
        logging.info("设备连接成功")

        return True

    @staticmethod
    def start_trace_thread():
        SeaOfStarsAW.trace_thread = iTraceThread()
        SeaOfStarsAW.trace_thread.start()

    @staticmethod
    def start_trace(path, case_name, scene_name, screenshot_path):
        time_stamp = time.strftime('%H%M%S', time.localtime())
        SeaOfStarsAW.trace_thread.start_trace(path, "{}-{}-{}".format(case_name, scene_name, time_stamp))
        SeaOfStarsAW.ut_device.screenshot(screenshot_path+'/'+case_name+scene_name+time_stamp+'.png')

    @staticmethod
    def stop_trace():
        SeaOfStarsAW.trace_thread.stop_trace()


    @staticmethod
    def get_app_list():
        result = os.popen('tidevice applist').read()
        app_list = result.split('\n')
        for index, app in enumerate(app_list):
            app_list[index] = app.split(' ')[0]
        return app_list

    @staticmethod
    def clear_background():
        result = os.popen('tidevice applist').read()
        app_list = result.split('\n')
        for index, app in enumerate(app_list):
            cur_app = app.split(' ')[0]
            command = 'tidevice kill '+cur_app
            os.popen(command)
            time.sleep(2)
        return True

    @staticmethod
    def check_status(**kw):
        if SeaOfStarsAW.ut_device(**kw).exists:
            logging.info('检测到元素存在-' + json.dumps(kw, ensure_ascii=False))
            return True
        time_stamp = time.strftime('%H%M%S', time.localtime())
        SeaOfStarsAW.ut_device.screenshot(SeaOfStarsAW.error_screenshot_path + '/' + SeaOfStarsAW.current_running_class_name + '_' + time_stamp + '.png')
        raise ElementNotFoundError('未找到元素-' + json.dumps(kw, ensure_ascii=False))

    @staticmethod
    def scroll_up(sleep_time = 5):
        # 上滑动作
        logging.info("上滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 500, 550, 2000, duration=0.04)
        time.sleep(sleep_time)

    @staticmethod
    def scroll_down(sleep_time = 5):
        # 下滑动作
        logging.info("下滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 2000, 550, 500, duration=0.01)
        time.sleep(sleep_time)

    # @staticmethod
    def swipe_left(sleep_time = 5):
        # 左滑动作
        logging.info("左滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, duration=0.03)
        time.sleep(sleep_time)


    @staticmethod
    def swipe_back(sleep_time = 3):
        # 侧滑返回动作
        logging.info("侧滑返回")
        SeaOfStarsAW.ut_device.swipe(20, 1950, 550, 1950, duration=0.03)
        time.sleep(sleep_time)
    def go_home(sleep_time = 2):


        Coordinates=SeaOfStarsAW.find_app_from_launcher('支付宝')
        while str(Coordinates) == ('Point(x=0, y=0)'):
            if SeaOfStarsAW.ut_device(label='不允许').exists:
                SeaOfStarsAW.ut_device(label='不允许').click()
            SeaOfStarsAW.ut_device.swipe_right()
            Coordinates = SeaOfStarsAW.find_app_from_launcher('支付宝')
    def swipe_to_launcher(sleep_time = 2):
        SeaOfStarsAW.ut_device.swipe(0.5,0.999,0.5,0.5)


    def write_results_to_excel(filename, sheetname, error_message):
        # 创建否则打开
        try:
            wb = openpyxl.load_workbook(filename)
            ws = wb.active
        except FileNotFoundError:
            wb = openpyxl.Workbook()
            ws = wb.active
        sheet = wb[sheetname] if sheetname in wb.sheetnames else wb.active
        # 写入表头
        ws['A1'] = 'TestCase'
        ws['B1'] = 'Result'
        # 判断是否有重复
        case_box = []
        if filename not in case_box:
            case_box.append(filename)
            row_number = sheet.max_row + 1
            sheet.cell(row=row_number, column=1, value=sheetname)
            sheet.cell(row=row_number, column=2, value=error_message)
            wb.save(filename)
        else:
            pass


class ElementNotFoundError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo


