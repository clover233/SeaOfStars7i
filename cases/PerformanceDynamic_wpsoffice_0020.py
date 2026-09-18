from aw import SeaOfStarsAW
from cases.wpsoffice_common import WpsOfficeCase


class PerformanceDynamic_wpsoffice_0020(WpsOfficeCase):
    """WPS 稻壳儿浏览、新建本地文字文档和文档浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            try:
                with self.capture_trace_5s(iteration, 1):
                    self.step(1, '启动WPS')
                    self.start_wps()
                self.step(2, '点击底部稻壳儿')
                self.open_docer()
                self.step(3, '滑动浏览稻壳儿页面，上滑两次、下滑两次')
                self.browse(2, 2)
                self.step(4, '点击首页，返回WPS首页')
                self.return_home()
                self.step(5, '文件列表滑动，上滑3次、下滑3次')
                self.browse(3, 3)
                self.step(6, '点击右下角红色+')
                self.open_new_menu()
                self.step(7, '点击文字icon')
                self.create_blank_word()
                self.step(8, '输入动态性能测试')
                self.input_document_text('动态性能测试')
                self.step(9, '点左上角保存按钮')
                self.open_save_as()
                self.step(10, '点击本机，进入保存页面')
                self.open_local_save_location()
                self.step(11, '点击文档文件夹')
                self.choose_document_folder()
                self.step(12, '点击右上角√进行保存')
                self.confirm_path_and_save()
                self.step(13, '返回首页')
                self.return_home()
                self.step(14, '点击一个文档进行浏览')
                self.open_created_document()
                self.step(15, '返回首页')
                self.back_from_document()
                self.return_home()
                with self.capture_trace_5s(iteration, 16):
                    self.step(16, '滑动返回Home页')
                    self.launcher()
            finally:
                # 中途断言失败时也恢复 WDA，避免后续用例一直保持 0/0。
                self._restore_idle_settings()
