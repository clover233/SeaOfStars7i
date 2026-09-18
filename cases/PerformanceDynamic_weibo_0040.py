from aw import SeaOfStarsAW
from cases.weibo_common import WeiboCase


class PerformanceDynamic_weibo_0040(WeiboCase):
    """微博用户搜索和九图草稿编辑（不发布）。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微博')
                self.start_weibo()
            self.step(2, '点击屏幕底部发现')
            self.tap_bottom_tab('发现')
            self.dismiss_optional_prompts()
            self.step(3, '点击搜索框')
            self.step(4, '输入动态测试')
            self.step(5, '点击搜索')
            self.open_discover_search('动态测试')
            self.step(6, '点击用户')
            self.step(7, '点击动态测试用户')
            self.choose_user_result('动态测试')
            self.step(8, '点击第一条微博，进行浏览')
            self.open_first_post()
            self.step(9, '返回微博首页')
            self.return_weibo_home()
            self.step(10, '点击右上角+')
            self.step(11, '点击写微博')
            self.open_compose()
            self.step(12, '输入今天天气很好')
            self.type_compose_text('今天天气很好')
            self.step(13, '点击图片图标')
            self.open_photo_picker()
            self.step(14, '选择9张图片')
            self.select_nine_photos()
            self.step(15, '点击下一步')
            self.next_photo_step()
            self.step(16, '点击下一步')
            self.next_photo_step()
            self.step(17, '返回微博主界面（放弃草稿，不发布）')
            self.abandon_compose_and_return_home()
            with self.capture_trace_5s(iteration, 18):
                self.step(18, '滑动返回Home页')
                self.launcher()
