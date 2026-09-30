"""离线验证采集步骤和 xctrace 停止流程，不连接或操作手机。"""

import ast
import importlib
from pathlib import Path
import signal
import tempfile
import unittest
from unittest.mock import Mock, patch

from aw import SeaOfStarsAW
from cases.CaseBase import Case
from cases.wda_case_common import WdaCase
from cases.alipay_common import AlipayCase
from cases.autonavi_common import AutonaviCase
from cases.PerformanceDynamic_fuzai import PerformanceDynamic_fuzai
from TraceTool.iTrace import iTraceThread


ROOT = Path(__file__).resolve().parents[1]


class TracePolicyTests(unittest.TestCase):
    def test_step_boundaries_and_repeated_iterations(self):
        for base in (WdaCase, AlipayCase, AutonaviCase):
            for last, expected in ((1, [1]), (2, [1, 2]), (3, [1, 2, 3]),
                                   (10, [1, 5, 10]), (15, [1, 8, 15])):
                with self.subTest(base=base.__name__, last=last):
                    cls = type('ExampleCase', (base,), {'TRACE_LAST_STEP': last})
                    events = []
                    with tempfile.TemporaryDirectory() as root, \
                            patch.object(SeaOfStarsAW, 'trace_thread', Mock()) as thread, \
                            patch.object(SeaOfStarsAW, 'start_trace',
                                         side_effect=lambda *a: events.append(a[2])), \
                            patch.object(SeaOfStarsAW, 'stop_trace',
                                         side_effect=lambda: events.append('saved')), \
                            patch('time.sleep'):
                        case = cls(root)
                        for iteration in range(2):
                            for number in range(1, last + 1):
                                if number in (1, last):
                                    with case.capture_trace(iteration, number):
                                        case.step(number, '测试动作')
                                else:
                                    case.step(number, '测试动作')
                            self.assertFalse(case._trace_active)
                        self.assertEqual(events, [event for _ in range(2)
                                                 for n in expected
                                                 for event in ('step_{}'.format(n), 'saved')])
                        self.assertEqual(thread.add_log.call_count, len(expected) * 2)

    def test_unselected_step_waits_for_previous_recording_before_ui_checks(self):
        cls = type('ExampleCase', (WdaCase,), {'TRACE_LAST_STEP': 10})
        events = []
        with tempfile.TemporaryDirectory() as root, \
                patch.object(SeaOfStarsAW, 'trace_thread', Mock()), \
                patch.object(SeaOfStarsAW, 'start_trace'), \
                patch.object(SeaOfStarsAW, 'stop_trace',
                             side_effect=lambda: events.append('saved')), \
                patch('time.sleep'):
            case = cls(root)
            case.step(5, '中间步骤')
            case.check_step_foreground = lambda n: events.append('next UI check')
            case.step(6, '非采集步骤')
            self.assertEqual(events, ['saved', 'next UI check'])
            self.assertFalse(case._trace_active)

    def test_context_saves_trace_on_action_failure(self):
        cls = type('ExampleCase', (WdaCase,), {'TRACE_LAST_STEP': 2})
        with tempfile.TemporaryDirectory() as root, \
                patch.object(SeaOfStarsAW, 'trace_thread', Mock()), \
                patch.object(SeaOfStarsAW, 'start_trace'), \
                patch.object(SeaOfStarsAW, 'stop_trace') as stop:
            case = cls(root)
            with self.assertRaisesRegex(RuntimeError, 'action failed'):
                with case.capture_trace(0, 1):
                    case.step(1, '启动')
                    raise RuntimeError('action failed')
            stop.assert_called_once()
            self.assertFalse(case._trace_active)

    def test_all_case_metadata_matches_existing_steps(self):
        count = 0
        for path in sorted((ROOT / 'cases').glob('PerformanceDynamic_*.py')):
            tree = ast.parse(path.read_text())
            module = importlib.import_module('cases.' + path.stem)
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue
                run = next((n for n in node.body if isinstance(n, ast.FunctionDef)
                            and n.name == 'run_case'), None)
                if run is None:
                    continue
                cls = getattr(module, node.name)
                numbers = {n.args[0].value for n in ast.walk(run)
                           if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                           and n.func.attr == 'step' and n.args
                           and isinstance(n.args[0], ast.Constant)}
                if not numbers:
                    self.assertIs(cls, PerformanceDynamic_fuzai)
                    continue
                with self.subTest(case=cls.__name__):
                    self.assertEqual(cls.TRACE_LAST_STEP, max(numbers))
                    selected = {1, (max(numbers) + 1) // 2, max(numbers)}
                    self.assertTrue(selected <= numbers)
                    case = cls.__new__(cls)
                    self.assertEqual({n for n in numbers if case.should_capture_step(n)}, selected)
                count += 1
        self.assertEqual(count, 142)

    def test_load_case_runs_all_apps_but_only_records_three(self):
        with tempfile.TemporaryDirectory() as root, \
                patch.object(SeaOfStarsAW, 'ut_device', Mock()) as device, \
                patch.object(SeaOfStarsAW, 'trace_thread', Mock()) as thread, \
                patch.object(SeaOfStarsAW, 'start_trace') as start, \
                patch.object(SeaOfStarsAW, 'stop_trace') as stop, \
                patch('time.sleep'):
            device.locked.return_value = False
            case = PerformanceDynamic_fuzai(root)
            case.run_case()
            self.assertEqual([call.args[2] for call in start.call_args_list],
                             ['step_1', 'step_8', 'step_16'])
            self.assertEqual(device.app_activate.call_count, 16)
            self.assertEqual(device.home.call_count, 16)
            self.assertEqual(thread.add_log.call_count, 3)
            self.assertEqual(stop.call_count, 3)

    def test_recording_timer_signals_and_saves_after_four_seconds(self):
        class WorkerFinished(Exception):
            pass

        process = Mock()
        process.poll.return_value = None
        process.wait.return_value = 0
        timer = Mock()

        def output():
            yield b'Recording started. Use Ctrl-C to stop.\n'
            # 只有读到真正开录提示之后才启动定时器。
            self.assertTrue(worker.realStartTrace)
            timer.start.assert_called_once()
            seconds, callback = timer_factory.call_args.args
            self.assertEqual(seconds, 4)
            callback()
            process.send_signal.assert_called_once_with(signal.SIGINT)
            yield b'Stopping recording...\n'

        def launch(command, **kwargs):
            self.assertEqual(command[command.index('--device-name') + 1], 'iphone17pm (26.0)')
            self.assertEqual(command[command.index('--time-limit') + 1], '600s')
            Path(command[command.index('--output') + 1]).mkdir()
            process.stdout = output()
            timer_factory.assert_not_called()
            return process

        with tempfile.TemporaryDirectory() as root, \
                patch('TraceTool.iTrace.xctrace_environment', return_value={}), \
                patch('TraceTool.iTrace.subprocess.Popen', side_effect=launch), \
                patch('TraceTool.iTrace.threading.Timer', return_value=timer) as timer_factory, \
                patch('TraceTool.iTrace.time.sleep', side_effect=WorkerFinished):
            worker = iTraceThread()
            worker.save_dir = root
            worker.save_name = 'example-step_1'
            worker.isLetTraceRun = True
            worker.command_finished.clear()
            with self.assertRaises(WorkerFinished):
                worker.run()
            self.assertTrue(worker.recording_finished.is_set())
            self.assertTrue(worker.command_finished.is_set())
            self.assertIsNone(worker.finish_error)
            self.assertFalse(worker.isLetTraceRun)
            self.assertEqual(len(list(Path(root).glob('example-step_1-*.trace'))), 1)
            timer.cancel.assert_called_once()
            process.wait.assert_called_once()


if __name__ == '__main__':
    unittest.main()
