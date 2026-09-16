from aw import SeaOfStarsAW
from cases.photo_common import PhotoCase


class PerformanceDynamic_photo_0030(PhotoCase):
    """Excel 7.0.2: browse media, create an album, then remove it."""

    ALBUM_NAME = '动态测试'

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动图库')
                self.start_photos()

            self.step(2, '点击相册，切换到相簿页')
            self.open_albums_page()

            self.step(3, '点击第一个非空图片相簿')
            album_label = self.open_album_node(self.first_nonempty_album())

            self.step(4, '图片相簿页向上抛滑5次，向下抛滑5次')
            self.fling_library(5, 5)

            self.step(5, '图片相簿页向上跟手滑5次，向下跟手滑5次')
            self.drag_library(5, 5)

            self.step(6, '进入图片相簿后侧滑返回，重复5次')
            self.back_to_albums()
            for _ in range(5):
                album = self.find_album(album_label)
                if album is None:
                    self.fail('重复浏览时未找到目标相簿：{}'.format(album_label))
                self.open_album_node(album)
                self.edge_back_from_album()

            self.step(7, '点击视频，进入视频合集页')
            self.open_media_types_page()
            self.open_videos()

            self.step(8, '点击第一个视频查看详情')
            self.open_first_album_asset(expected='video')

            self.step(9, '点击右下角删除图标，并在提示框中确认删除')
            self.delete_open_video()

            self.step(10, '返回相簿界面')
            self.return_from_videos_to_albums()

            self.step(11, '点击新建，拉起新建相簿页')
            self.ensure_album_absent(self.ALBUM_NAME)
            self.open_new_album_form()

            self.step(12, '设置新建相簿名称为动态测试后确认')
            self.create_album(self.ALBUM_NAME)

            self.step(13, '浏览文件选择器的照片和精选集分页，各上滑5次、下滑5次')
            self.open_named_album(self.ALBUM_NAME)
            self.open_album_picker()
            self.browse_picker()

            self.step(14, '选择第一个文件后，点击 X 取消')
            self.select_first_picker_asset_and_cancel()

            self.step(15, '长按动态测试相簿，点击删除相簿并确认')
            self.delete_named_album(self.ALBUM_NAME)

            self.step(16, '返回图库主界面')
            self.return_to_library_main()

            with self.capture_trace_5s(iteration, 17):
                self.step(17, '滑动返回 Home 页')
                self.launcher()
