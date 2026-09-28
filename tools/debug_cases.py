"""通过现有 WDA 定向调试用例，保留每一步截图/XML，不采集性能 trace。"""
import argparse
import base64
import importlib
import json
import logging
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aw import SeaOfStarsAW
from cases.wda_case_common import WdaCase
from cases.alipay_common import AlipayCase


def debug_step(self, number, text):
    self.current_step = '{}、{}'.format(number, text)
    if hasattr(self, 'check_step_foreground'):
        self.check_step_foreground(number)
    if self._has_step:
        time.sleep(self.STEP_INTERVAL)
    self._has_step = True
    logging.info(self.current_step)
    if not self._debug_capture_steps:
        return
    path = Path(self.screenshot_dir_path) / 'step_{}'.format(number)
    self.device.screenshot(str(path.with_suffix('.png')))
    path.with_suffix('.xml').write_text(self.device.source(), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cases', nargs='+', help='完整用例类名，按顺序串行执行')
    parser.add_argument('--result', default='Result/debug_' + time.strftime('%Y%m%d_%H%M%S'))
    parser.add_argument('--failure-only', action='store_true',
                        help='只在失败时保存截图/XML，减少定向复跑的额外等待')
    args = parser.parse_args()
    # 先验证全部名称，避免拼写错误时已经开始操作设备。
    classes = []
    for name in args.cases:
        if not name.startswith('PerformanceDynamic_') or not name.isidentifier():
            parser.error('非法用例名：' + name)
        classes.append(getattr(importlib.import_module('cases.' + name), name))
    root = Path(args.result).resolve()
    root.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler(root / 'debug.log')])
    SeaOfStarsAW.init_device()
    originals = [(base, base.step, base._start_step_trace)
                 for base in (WdaCase, AlipayCase)]
    for base, _, _ in originals:
        base.step = debug_step
        base._start_step_trace = lambda self, number: None
    results = []
    try:
        for cls in classes:
            case = cls(str(root))
            case.TEST_TIME = 1
            case._debug_capture_steps = not args.failure_only
            row = {'case': cls.__name__, 'artifacts': case.result_dir_path}
            try:
                case.set_up()
                case.run_case()
                row['status'] = 'PASS'
            except KeyboardInterrupt:
                row.update(status='INTERRUPTED', step=case.current_step,
                           error='调试已暂停')
                results.append(row)
                (root / 'summary.json').write_text(
                    json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
                raise
            except Exception as error:
                logging.exception('用例调试失败')
                row.update(status='FAIL', step=case.current_step, error=str(error))
                try:
                    path = Path(case.screenshot_dir_path)
                    screenshot = case.device.http.get('screenshot', timeout=8).value
                    (path / 'failed.png').write_bytes(base64.b64decode(screenshot))
                except Exception:
                    logging.exception('保存失败截图失败')
                try:
                    source = case.device.http.get('source?format=xml', timeout=8).value
                    (Path(case.screenshot_dir_path) / 'failed.xml').write_text(
                        source, encoding='utf-8')
                except Exception:
                    logging.exception('保存失败页面层级失败')
            finally:
                if hasattr(case, '_restore_idle_settings'):
                    case._restore_idle_settings()
            if getattr(case, 'skipped_steps', None):
                row['skipped_steps'] = case.skipped_steps
            logging.info('%s %s', row['status'], cls.__name__)
            results.append(row)
            (root / 'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    finally:
        for base, step, trace in originals:
            base.step, base._start_step_trace = step, trace
    return 1 if any(row['status'] == 'FAIL' for row in results) else 0


if __name__ == '__main__':
    sys.exit(main())
