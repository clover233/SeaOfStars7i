import os
import threading
import time
import logging
import signal
import subprocess

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
        self.process = None
        self.realStartTrace = False
        self.start_time = None
        self.log_path = None

    def start_trace(self, trace_dir, trace_name):
        self.save_dir = trace_dir
        self.save_name = trace_name
        self.isLetTraceRun = True
        self.process = None
        # 等待Trace真正采集
        while not self.realStartTrace:
            time.sleep(0.1)

    def stop_trace(self):
        if self.process:
            self.isLetTraceRun = False
            # ctrl-c方式停止🤚
            os.kill(self.process.pid, signal.SIGINT)
            tips_bool = True
            # 等待Trace抓取完成
            while self.process:
                if tips_bool:
                    logging.info("等待Trace抓取结束中...")
                    tips_bool = False
                time.sleep(0.1)
        else:
            logging.info("Trace进程未运行！无需停止.")

    def run(self):
        global start_time_stamp, capture_time
        logging.info("trace线程开始运行")
        while 1:
            tips_bool = False
            while self.isLetTraceRun:
                # 开始抓取Trace
                tips_bool = True
                logging.info("trace线程开始抓取trace")
                end_time = None
                time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                temptrace_path = os.path.join(self.save_dir, "temp_{}.trace".format(time_stamp))
                self.log_path = os.path.join(self.save_dir, "temp_{}.log".format(time_stamp))
                if os.path.exists(self.log_path):
                    os.remove(self.log_path)
                # command = ['xctrace', 'record', '--device-name', 'iPhone (16.3.1)', '--template', 'UX-HitchAndMetal',
                #            '--all-processes', '--output', temptrace_path, "--time-limit", '410s']
                command = ['xctrace', 'record', '--device-name', 'iPhoned (18.5)', '--template',
                           'UX-HitchAndMetal','--all-processes', '--output', temptrace_path, "--time-limit", '410s']
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while self.process.poll() is None:
                    line = self.process.stdout.readline().strip().decode("utf8")
                    if line != '':
                        if "Ctrl-C" in line:
                            # trace真正开始的时间
                            self.start_time = time.time()
                            start_time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())

                            self.realStartTrace = True
                        if "Stopping recording" in line:
                            # trace真正结束的时间
                            end_time = time.time()
                        logging.info(line)
                self.process = None
                self.realStartTrace = False
                try:
                    capture_time = time.time() - self.start_time
                except:
                    pass
                if end_time:
                    # 真正的采集时间
                    capture_time = end_time - self.start_time
                # 重命名文件 - 等待2秒保证文件完全生成,通过线程避免阻塞
                new_trace_name = "{}-{}({}s).trace".format(self.save_name, start_time_stamp, int(capture_time))
                new_trace_path = os.path.join(self.save_dir, new_trace_name)
                new_log_name = "{}-{}({}s).log".format(self.save_name, start_time_stamp, int(capture_time))
                new_log_path = os.path.join(self.save_dir, new_log_name)
                rename_file = lambda src, dst: os.rename(src, dst)
                timer = threading.Timer(2, rename_file, [temptrace_path, new_trace_path])
                timer.start()
                timer = threading.Timer(2, rename_file, [self.log_path, new_log_path])
                timer.start()
                self.start_time = None
                # os.rename(trace_path, new_trace_path)
            if tips_bool:
                logging.info("等待trace抓取命令......")

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

