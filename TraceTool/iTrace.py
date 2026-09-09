import os
import threading
import time
import logging
import signal
import subprocess
from pathlib import Path

def xctrace_environment():
    """保留显式配置；系统仅有CommandLineTools时查找完整Xcode。"""
    env = os.environ.copy()
    if env.get('DEVELOPER_DIR'):
        return env
    selected = subprocess.run(
        ['/usr/bin/xcode-select', '-p'], capture_output=True, text=True)
    developer_dir = Path(selected.stdout.strip())
    if selected.returncode == 0 and (developer_dir / 'usr/bin/xctrace').is_file():
        return env
    for directory in (Path('/Applications'), Path.home() / 'Applications',
                      Path.home() / 'Downloads'):
        for app in sorted(directory.glob('Xcode*.app')):
            developer_dir = app / 'Contents/Developer'
            if (developer_dir / 'usr/bin/xctrace').is_file():
                env['DEVELOPER_DIR'] = str(developer_dir)
                logging.info('Trace使用Xcode路径: %s', developer_dir)
                return env
    raise OSError('未找到完整Xcode，请安装Xcode或设置DEVELOPER_DIR为其Contents/Developer路径')


class iTraceThread(threading.Thread):

    def __init__(self):
        # Trace worker must not keep the whole test process alive after all
        # selected cases have finished.
        threading.Thread.__init__(self, daemon=True)
        self.isLetTraceRun = False
        self.process = None
        self.realStartTrace = False
        self.start_time = None
        self.log_path = None
        self.start_error = None

    def start_trace(self, trace_dir, trace_name):
        self.save_dir = trace_dir
        self.save_name = trace_name
        self.start_error = None
        self.realStartTrace = False
        self.isLetTraceRun = True
        self.process = None
        # 等待Trace真正采集
        while not self.realStartTrace:
            if self.start_error:
                raise RuntimeError(self.start_error)
            if not self.is_alive():
                raise RuntimeError('Trace线程已退出，无法启动采集')
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
        logging.info("trace线程开始运行")
        while 1:
            tips_bool = False
            while self.isLetTraceRun:
                # 开始抓取Trace
                tips_bool = True
                logging.info("trace线程开始抓取trace")
                end_time = None
                start_time_stamp = None
                self.start_time = None
                time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                temptrace_path = os.path.join(self.save_dir, "temp_{}.trace".format(time_stamp))
                self.log_path = os.path.join(self.save_dir, "temp_{}.log".format(time_stamp))
                if os.path.exists(self.log_path):
                    os.remove(self.log_path)
                # command = ['xctrace', 'record', '--device-name', 'iPhone (16.3.1)', '--template', 'UX-HitchAndMetal',
                #            '--all-processes', '--output', temptrace_path, "--time-limit", '410s']
                template_path = Path(__file__).resolve().parent / 'Templates' / 'ActivityMonitor.tracetemplate'
                command = ['xctrace', 'record', '--device-name', 'iPhone17PM (26.0)', '--template',
                           str(template_path), '--all-processes', '--output', temptrace_path, "--time-limit", '410s']
                try:
                    if not template_path.is_file():
                        raise FileNotFoundError('采集模板不存在: {}'.format(template_path))
                    self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                    env=xctrace_environment())
                except OSError as err:
                    self.start_error = '无法启动xctrace: {}'.format(err)
                    self.isLetTraceRun = False
                    break
                output_lines = []
                for raw_line in self.process.stdout:
                    line = raw_line.strip().decode("utf8", errors="replace")
                    if line != '':
                        output_lines.append(line)
                        if "Ctrl-C" in line:
                            # trace真正开始的时间
                            self.start_time = time.time()
                            start_time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())

                            self.realStartTrace = True
                        if "Stopping recording" in line:
                            # trace真正结束的时间
                            end_time = time.time()
                        logging.info(line)
                return_code = self.process.wait()
                self.process = None
                self.realStartTrace = False
                if start_time_stamp is None:
                    self.start_error = 'xctrace未开始采集（退出码{}）: {}'.format(
                        return_code, '\n'.join(output_lines))
                    self.isLetTraceRun = False
                    logging.error(self.start_error)
                    break
                capture_time = time.time() - self.start_time
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
            time.sleep(0.1)

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
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
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
