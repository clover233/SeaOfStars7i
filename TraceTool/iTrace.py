import os
import signal
import threading
import time
import logging
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

    # TRACE_TEMPLATE = 'Activity Monitor'
    TRACE_TEMPLATE = 'UX-HitchAndMetal'

    # xctrace 自身的安全上限保持默认 600s；实际短采集由 5s 定时器主动，发送 SIGINT 结束，避免依赖过短的 --time-limit 生成不完整文档。
    TRACE_TIME_LIMIT_SECONDS = 600
    TRACE_CAPTURE_SECONDS = 5

    def __init__(self):
        threading.Thread.__init__(self)
        self.isLetTraceRun = False
        self.process = None
        self.realStartTrace = False
        self.start_time = None
        self.log_path = None
        self.start_error = None
        self.finish_error = None
        self.recording_finished = threading.Event()
        self.command_finished = threading.Event()
        self.command_finished.set()

    def start_trace(self, trace_dir, trace_name):
        # 防止两个 xctrace 命令并发运行；正常情况下 stop_trace 会等上一份
        # 完整保存，这里仍保留等待作为安全保护。
        if not self.command_finished.is_set():
            logging.info('等待上一份 Trace 保存完成...')
        self.command_finished.wait()
        self.command_finished.clear()
        self.recording_finished.clear()
        self.save_dir = trace_dir
        self.save_name = trace_name
        self.start_error = None
        self.finish_error = None
        self.realStartTrace = False
        self.process = None
        # 请求标志最后写入，避免工作线程先启动进程又被这里清空。
        self.isLetTraceRun = True
        # 等待Trace真正采集
        while not self.realStartTrace:
            if self.start_error:
                raise RuntimeError(self.start_error)
            if not self.is_alive():
                raise RuntimeError('Trace线程已退出，无法启动采集')
            time.sleep(0.1)

    def stop_trace(self):
        if self.command_finished.is_set():
            if self.finish_error:
                raise RuntimeError(self.finish_error)
            logging.info("Trace进程未运行！无需停止.")
            return

        # 每个用例都通过公共入口执行到这里。即使用例步骤早于 5s 完成，
        # 也等定时器在实际开录约 5s 后主动停止；随后等待 xctrace 完整落盘。
        if not self.recording_finished.is_set():
            logging.info("等待约%ss后停止 Trace...", self.TRACE_CAPTURE_SECONDS)
        self.recording_finished.wait()
        self.command_finished.wait()
        if self.finish_error:
            raise RuntimeError(self.finish_error)
        logging.info("Trace 已停止并完成保存")

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
                stop_timer = None
                self.start_time = None
                time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                temptrace_path = os.path.join(self.save_dir, "temp_{}.trace".format(time_stamp))
                self.log_path = os.path.join(self.save_dir, "temp_{}.log".format(time_stamp))
                if os.path.exists(self.log_path):
                    os.remove(self.log_path)
                Path(self.log_path).touch()
                # command = ['xctrace', 'record', '--device-name', 'iPhone (16.3.1)', '--template', 'UX-HitchAndMetal',
                #            '--all-processes', '--output', temptrace_path, "--time-limit", '410s']
                command = ['xctrace', 'record', '--device-name', 'iPhone17 (26.6.1)', '--template',
                           self.TRACE_TEMPLATE, '--all-processes', '--output', temptrace_path, "--time-limit",
                           '{}s'.format(self.TRACE_TIME_LIMIT_SECONDS)]
                try:
                    self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                    env=xctrace_environment())
                except OSError as err:
                    self.start_error = '无法启动xctrace: {}'.format(err)
                    self.isLetTraceRun = False
                    self.recording_finished.set()
                    self.command_finished.set()
                    break
                output_lines = []
                for raw_line in self.process.stdout:
                    line = raw_line.strip().decode("utf8", errors="replace")
                    if line != '':
                        output_lines.append(line)
                        if "Ctrl-C" in line and self.start_time is None:
                            # trace真正开始的时间
                            self.start_time = time.time()
                            start_time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())

                            self.realStartTrace = True
                            # --time-limit 保持 600s 作为安全上限；实际开录约
                            # 5s 后主动 Ctrl-C，让 xctrace 走正常停止/保存流程。
                            process = self.process
                            def stop_after_capture():
                                if process and process.poll() is None:
                                    logging.info(
                                        'Trace已采集约%ss，调用停止流程',
                                        self.TRACE_CAPTURE_SECONDS)
                                    self.isLetTraceRun = False
                                    try:
                                        process.send_signal(signal.SIGINT)
                                    except OSError:
                                        logging.exception('Trace停止信号发送失败')
                            stop_timer = threading.Timer(
                                self.TRACE_CAPTURE_SECONDS,
                                stop_after_capture)
                            stop_timer.start()
                        if ("Stopping recording" in line
                                or "Reached specified time limit" in line):
                            # trace真正结束的时间
                            end_time = time.time()
                            self.recording_finished.set()
                        logging.info(line)
                return_code = self.process.wait()
                if stop_timer is not None:
                    stop_timer.cancel()
                self.process = None
                self.realStartTrace = False
                # 定时主动停止时 stop_trace 可能尚未被调用，不能因为
                # isLetTraceRun 仍为 True 而紧接着开始第二份 trace。
                self.isLetTraceRun = False
                self.recording_finished.set()
                if start_time_stamp is None:
                    self.start_error = 'xctrace未开始采集（退出码{}）: {}'.format(
                        return_code, '\n'.join(output_lines))
                    self.isLetTraceRun = False
                    logging.error(self.start_error)
                    self.command_finished.set()
                    break
                capture_time = time.time() - self.start_time
                if end_time:
                    # 真正的采集时间
                    capture_time = end_time - self.start_time
                # process.wait() 返回表示 xctrace 已完成落盘，此时同步重命名；
                # stop_trace 只有在重命名完成后才会返回。
                new_trace_name = "{}-{}({}s).trace".format(self.save_name, start_time_stamp, int(capture_time))
                new_trace_path = os.path.join(self.save_dir, new_trace_name)
                new_log_name = "{}-{}({}s).log".format(self.save_name, start_time_stamp, int(capture_time))
                new_log_path = os.path.join(self.save_dir, new_log_name)
                try:
                    os.rename(temptrace_path, new_trace_path)
                    os.rename(self.log_path, new_log_path)
                except OSError as err:
                    self.finish_error = 'Trace保存或重命名失败: {}'.format(err)
                    logging.exception(self.finish_error)
                finally:
                    self.start_time = None
                    self.command_finished.set()
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
    # 实际开录约5s后主动停止，并等待输出文件完整保存
    t_thread.stop_trace()
