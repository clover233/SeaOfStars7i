import time
import os
from contextlib import contextmanager
from aw import SeaOfStarsAW

class Case(object):
    # 用例的最后一个 step 编号；新增或调整步骤时同步更新。
    TRACE_LAST_STEP = None

    def __init__(self, result_path):
        self._trace_active = False
        self._trace_step_number = None
        self._trace_iteration = 0
        time_stamp = time.strftime('%H%M%S', time.localtime())
        self.result_dir_path = os.path.join(result_path, self.__class__.__name__+'_'+time_stamp)
        self.trace_dir_path = os.path.join(self.result_dir_path, 'Traces')
        self.screenshot_dir_path = os.path.join(self.result_dir_path, 'Screenshots')
        SeaOfStarsAW.error_screenshot_path = self.screenshot_dir_path
        SeaOfStarsAW.public_screen_shot_dir = self.screenshot_dir_path
        os.makedirs(self.trace_dir_path)
        os.makedirs(self.screenshot_dir_path)

    def should_capture_step(self, step_number):
        last = self.TRACE_LAST_STEP
        if not isinstance(last, int) or last < 1:
            raise ValueError('{} 必须设置 TRACE_LAST_STEP'.format(self.__class__.__name__))
        return step_number in {1, (last + 1) // 2, last}

    @contextmanager
    def capture_trace(self, iteration, step_number):
        """收尾显式步骤；开录与时长由 step 和统一采集线程控制。"""
        self._trace_iteration = iteration
        if step_number == 1:
            self._has_step = False
        try:
            yield
        finally:
            if self._trace_step_number == step_number:
                self._stop_step_trace()

    def _stop_step_trace(self):
        if self._trace_active:
            try:
                SeaOfStarsAW.stop_trace()
            finally:
                self._trace_active = False
                self._trace_step_number = None

    def _start_step_trace(self, step_number):
        """仅采集首步、向上取整的中间步和末步，进入下一步前完成保存。"""
        self._stop_step_trace()
        if not self.should_capture_step(step_number):
            return
        if SeaOfStarsAW.trace_thread is None:
            SeaOfStarsAW.start_trace_thread()
        SeaOfStarsAW.start_trace(
            self.trace_dir_path,
            self.__class__.__name__,
            'step_{}'.format(step_number),
            self.screenshot_dir_path,
        )
        self._trace_active = True
        self._trace_step_number = step_number
