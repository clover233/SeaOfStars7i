import logging
import time
import os
from aw import SeaOfStarsAW

class Case(object):
    def __init__(self, result_path):
        time_stamp = time.strftime('%H%M%S', time.localtime())
        self.result_dir_path = os.path.join(result_path, self.__class__.__name__+'_'+time_stamp)
        self.trace_dir_path = os.path.join(self.result_dir_path, 'Traces')
        self.screenshot_dir_path = os.path.join(self.result_dir_path, 'Screenshots')
        SeaOfStarsAW.error_screenshot_path = self.screenshot_dir_path
        SeaOfStarsAW.public_screen_shot_dir = self.screenshot_dir_path
        os.makedirs(self.trace_dir_path)
        os.makedirs(self.screenshot_dir_path)
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.fh = logging.FileHandler(os.path.join(self.result_dir_path, 'log.txt'), encoding='utf-8')
        self.fh.setFormatter(formatter)
        logger.addHandler(self.fh)
