#!/usr/bin/env python3
"""Keep a go-ios tunnel, WDA runner and localhost:8100 forward alive.

Run from a normal user shell. This script asks sudo once for the tunnel and
remoted; run the test suite separately after it reports WDA ready.
"""

import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
IOS = ROOT / "tools" / "ios"
UDID = os.environ.get("IOS_UDID", "00008130-0009146104298D3A")
LOG_DIR = ROOT / "Result" / "wda_supervisor"
CHECK_SECONDS = 10
READY_SECONDS = 90
MAX_RESTARTS = 5
WDA_BUNDLE = "cn.wangzijian.WebDriverAgentRunner.xctrunner"


def say(message):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), message, flush=True)


def sudo(*args, interactive=False):
    command = ["sudo"] if interactive else ["sudo", "-n"]
    return subprocess.run(command + list(args), check=True)


def port_in_use():
    with socket.socket() as connection:
        connection.settimeout(1)
        return connection.connect_ex(("127.0.0.1", 8100)) == 0


def device_attached():
    try:
        result = subprocess.run([str(IOS), "list"], capture_output=True,
                                text=True, timeout=10, check=True)
        return UDID in result.stdout
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def tunnel_ready():
    try:
        result = subprocess.run([str(IOS), "tunnel", "ls"], capture_output=True,
                                text=True, timeout=5, check=True)
        return UDID in result.stdout
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def wda_healthy():
    try:
        with urlopen("http://127.0.0.1:8100/status", timeout=3) as response:
            if response.status != 200:
                return False
            status = json.load(response)
            return status.get("value", {}).get("ready") is True
    except (OSError, ValueError, TypeError):
        return False


def spawn(name, command, new_session=True):
    path = LOG_DIR / f"{name}.log"
    with path.open("ab", buffering=0) as log:
        log.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 启动 {name}\n".encode())
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=new_session)
    process.owns_group = new_session
    say(f"已启动 {name}，PID {process.pid}，日志 {path}")
    return process


def stop(process):
    if process.poll() is not None:
        return
    try:
        if process.owns_group:
            os.killpg(process.pid, signal.SIGTERM)
        else:
            # sudo must retain the current terminal's credential timestamp.
            # It therefore shares our session and must not receive killpg().
            process.terminate()
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            if process.owns_group:
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.wait()


def stop_stack(processes):
    for process in reversed(processes):
        stop(process)
    processes.clear()


def ensure_developer_image():
    cache = LOG_DIR / "devimages"
    cache.mkdir(exist_ok=True)
    path = LOG_DIR / "image.log"
    say("检查并挂载开发者镜像")
    with path.open("ab", buffering=0) as log:
        log.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] image auto\n".encode())
        try:
            result = subprocess.run([
                str(IOS), f"--udid={UDID}", "image", "auto",
                f"--basedir={cache}",
            ], stdout=log, stderr=subprocess.STDOUT, timeout=300)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(f"开发者镜像挂载超时；请查看 {path}") from error
    if result.returncode != 0:
        raise RuntimeError(f"开发者镜像挂载失败；请查看 {path}")


def start_stack(processes):
    ensure_developer_image()
    tunnel = spawn("tunnel", [
        "sudo", "-n", str(IOS), f"--udid={UDID}", "tunnel", "start",
    ], new_session=False)
    processes.append(tunnel)
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if tunnel.poll() is not None:
            say(f"隧道进程退出，退出码 {tunnel.returncode}；请查看 tunnel.log")
            return False
        if tunnel_ready():
            break
        time.sleep(2)
    else:
        say("隧道 45 秒内未就绪；请查看 tunnel.log")
        return False

    processes.append(spawn("runwda", [
        str(IOS), f"--udid={UDID}", "runwda",
        f"--bundleid={WDA_BUNDLE}",
        f"--testrunnerbundleid={WDA_BUNDLE}",
        "--xctestconfig=WebDriverAgentRunner.xctest",
    ]))
    time.sleep(2)
    processes.append(spawn("forward", [
        str(IOS), f"--udid={UDID}", "forward", "8100", "8100",
    ]))
    return True


def main():
    if not IOS.is_file():
        raise RuntimeError(f"找不到 go-ios：{IOS}")
    if port_in_use():
        raise RuntimeError("本机 8100 已被占用；请先关闭旧的端口转发")
    if not device_attached():
        raise RuntimeError(f"go-ios 未发现设备 {UDID}；请检查 USB、解锁和信任提示")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    say("验证 sudo 权限；此处可能要求输入密码")
    sudo("-v", interactive=True)

    remoted_pids = subprocess.check_output(["pgrep", "-x", "remoted"], text=True).split()
    for pid in remoted_pids:
        state = subprocess.check_output(["ps", "-o", "state=", "-p", pid], text=True).strip()
        if state.startswith("T"):
            raise RuntimeError("remoted 已被手动暂停；请先恢复，再单独运行本脚本")

    processes = []
    remoted_paused = False
    last_sudo_refresh = time.monotonic()
    try:
        sudo("pkill", "-SIGSTOP", "-x", "remoted")
        remoted_paused = True
        say("已暂停 remoted")

        restarts = 0
        while True:
            sudo("-v")
            last_sudo_refresh = time.monotonic()
            started = start_stack(processes)
            deadline = time.monotonic() + READY_SECONDS
            ready = False
            while started and time.monotonic() < deadline:
                exited = [process for process in processes if process.poll() is not None]
                if exited:
                    say("启动失败：" + ", ".join(
                        f"PID {process.pid} 退出码 {process.returncode}" for process in exited))
                    break
                if wda_healthy():
                    say("WDA 已就绪：http://127.0.0.1:8100/status；现在可启动测试")
                    ready = True
                    break
                time.sleep(2)
            if started and not ready and time.monotonic() >= deadline:
                say("等待 WDA 就绪超时")

            failures = 0
            while ready:
                if time.monotonic() - last_sudo_refresh >= 60:
                    sudo("-v")
                    last_sudo_refresh = time.monotonic()
                if any(process.poll() is not None for process in processes):
                    break
                if wda_healthy():
                    failures = 0
                    restarts = 0
                else:
                    failures += 1
                    if failures >= 3:
                        break
                    say(f"WDA 健康检查失败（{failures}/3），等待再次确认")
                time.sleep(CHECK_SECONDS)

            say("WDA、转发或隧道不可用，准备重建连接")
            stop_stack(processes)
            restarts += 1
            if restarts > MAX_RESTARTS:
                raise RuntimeError(f"连续重建超过 {MAX_RESTARTS} 次，请查看 {LOG_DIR} 中的日志")
            time.sleep(min(5 * restarts, 30))
    finally:
        try:
            stop_stack(processes)
        finally:
            if remoted_paused:
                sudo("pkill", "-SIGCONT", "-x", "remoted")
                say("已恢复 remoted")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("收到 Ctrl+C，停止监控")
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        say(f"监控停止：{error}")
        sys.exit(1)
