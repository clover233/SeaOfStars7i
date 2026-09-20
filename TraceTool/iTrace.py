import os
import threading
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logging.getLogger('matplotlib.font_manager').disabled = True
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)


class iTraceThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.isLetTraceRun = False
        self.realStartTrace = False
        self.start_time = None
        self.log_path = None
        self._stop_event = threading.Event()

    def start_trace(self, trace_dir, trace_name):
        self.save_dir = trace_dir
        self.save_name = trace_name
        self._stop_event.clear()
        self.isLetTraceRun = True
        # 等待日志采集真正开始
        while not self.realStartTrace:
            time.sleep(0.1)

    def stop_trace(self):
        if self.isLetTraceRun:
            self.isLetTraceRun = False
            self._stop_event.set()
            logging.info("日志采集停止.")
        else:
            logging.info("日志采集未运行！无需停止.")

    def run(self):
        global start_time_stamp, capture_time
        logging.info("日志线程开始运行")
        while 1:
            tips_bool = False
            while self.isLetTraceRun:
                tips_bool = True
                logging.info("日志线程开始采集日志")
                time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                self.log_path = os.path.join(self.save_dir, "temp_{}.log".format(time_stamp))
                if os.path.exists(self.log_path):
                    os.remove(self.log_path)
                # 记录开始时间
                self.start_time = time.time()
                start_time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                self.realStartTrace = True
                logging.info("日志采集已开始")
                # 等待stop_trace被调用
                self._stop_event.wait()
                end_time = time.time()
                self.realStartTrace = False
                try:
                    capture_time = end_time - self.start_time
                except:
                    pass
                # 重命名log文件
                new_log_name = "{}-{}({}s).log".format(self.save_name, start_time_stamp, int(capture_time))
                new_log_path = os.path.join(self.save_dir, new_log_name)
                def rename_file(src, dst):
                    if not os.path.exists(src):
                        logging.warning("重命名跳过，源文件不存在: {}".format(src))
                        return
                    if os.path.exists(dst):
                        logging.warning("重命名跳过，目标已存在: {}".format(dst))
                        return
                    os.rename(src, dst)
                timer = threading.Timer(2, rename_file, [self.log_path, new_log_path])
                timer.start()
                self.start_time = None
            if tips_bool:
                logging.info("等待日志采集命令......")

    # kargs为场景动作参数,比如入参为 抖音,应用启动,  最后会以[抖音][应用启动]形式保存, 建议至少两个参数, 参数数量尽量保持一致
    def add_log(self, *kargs):
        if self.start_time:
            content = "".join(["["+i +"]" for i in kargs])
            logging.info("trace 同步日志内容 {}".format(content))
            time_end = time.time()
            time_past = "%.6f" % (time_end-self.start_time)
            with open(self.log_path, 'a+', encoding="utf-8") as file:
                file.writelines("{} : {}".format(time_past, content))
        else:
            logging.error("trace not start")


if __name__ == "__main__":
    # trace抓取线程启动
    t_thread = iTraceThread()
    t_thread.start()

    # 开始抓取, 保存目录，trace名
    t_thread.start_trace(".", "test")
    # 执行ui操作, 每次时间不能超过300秒
    time.sleep(2)
    t_thread.add_log("抖音", "应用启动")
    time.sleep(3)
    # 停止抓取 - 这里会根据抓取时间，会等待10s-80s左右
    t_thread.stop_trace()
