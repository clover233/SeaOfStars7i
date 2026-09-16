from aw import SeaOfStarsAW
from cases.setting_common import SettingCase


class PerformanceDynamic_setting_0010(SettingCase):
    """将 Android/华为设置步骤映射为不改变配置的 iOS 等价浏览。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动设置')
                self.start_settings()

            self.step(2, '设置首页上滑2次、下滑2次')
            self.browse(2, 2)
            self.return_to_root()

            self.step(3, '点击 Apple 账户，进入账户页面')
            self.open_apple_account()

            self.step(4, '返回设置主页面')
            self.close_apple_account()
            self.return_to_root()

            self.step(5, '进入通用/关于本机页面')
            self.tap_scrolling('通用', 'General', wait=3)
            self.tap_scrolling('关于本机', 'About', wait=3)

            self.step(6, '返回设置主页面')
            self.return_to_root()

            self.step(7, '点击 Wi-Fi')
            self.tap_scrolling('Wi-Fi', '无线局域网', 'WIFI', wait=4)

            self.step(8, 'Wi-Fi 页面上滑1次、下滑1次')
            self.browse(1, 1)

            self.step(9, '返回设置首页')
            self.return_to_root()

            self.step(10, '点击显示与亮度')
            self.tap_scrolling('显示与亮度', 'Display & Brightness',
                               'DISPLAY', wait=4)

            self.step(11, '亮度进度条右拉一次、左拉一次')
            self.drag_brightness()

            self.step(12, '返回设置首页')
            self.return_to_root()

            self.step(13, '点击声效与触感反馈（声音与触感等价项）')
            self.tap_scrolling('声效与触感反馈', '声音与触感',
                               'Sounds & Haptics', 'Sounds',
                               'com.apple.settings.sounds', wait=4)

            self.step(14, '点击短信铃声')
            # iOS 26 中文界面显示“短信铃声”，其稳定 identifier 为
            # Text_Messages；优先按 identifier 定位，避免滚动搜索退出子页。
            self.tap_scrolling('Text_Messages', '短信铃声',
                               '信息铃声', 'Text Tone', wait=4)

            self.step(15, '短信铃声页面上滑2次、下滑2次')
            self.browse(2, 2)

            self.step(16, '返回设置首页')
            self.return_to_root()

            self.step(17, '进入墙纸（iOS 桌面和个性化等价项）')
            self.open_wallpaper_settings()

            self.step(18, '进入添加新墙纸（更多主题等价项）')
            self.open_new_wallpaper()

            self.step(19, '浏览第一组墙纸候选（替代萌主跳跳）')
            self.browse_wallpaper_candidates(1, 1)

            self.step(21, '滑动返回 Home 页')
            self.launcher()

            self.step(22, 'Home 页左滑3次、右滑3次')
            self.home_page_browse()

            self.step(23, '启动设置')
            self.start_settings()

            self.step(24, '再次进入墙纸/添加新墙纸')
            self.open_wallpaper_gallery()

            self.step(25, '浏览第二组墙纸候选（替代萌主嘿嘿）')
            self.browse_wallpaper_candidates(2, 1)

            self.step(27, '滑动返回 Home 页')
            self.launcher()

            self.step(28, 'Home 页左滑3次、右滑3次')
            self.home_page_browse()

            self.step(29, '启动设置')
            self.start_settings(root=False)

            self.step(30, '返回设置主界面')
            self.return_to_root()

            self.step(31, '点击通用/iPhone 储存空间')
            self.tap_scrolling('通用', 'General', wait=3)
            self.tap_scrolling('iPhone 储存空间', 'iPhone Storage',
                               'STORAGE_MGMT', wait=8)

            self.step(32, 'iPhone 储存空间页面上滑2次、下滑2次')
            self.browse(2, 2)

            self.step(33, '返回设置主界面')
            self.return_to_root()

            self.step(34, '点击电池，进入电池页面')
            self.tap_scrolling('电池', 'Battery', 'BATTERY_USAGE', wait=5)

            self.step(35, '返回设置主界面')
            self.return_to_root()

            with self.capture_trace_5s(iteration, 36):
                self.step(36, '滑动返回 Home 页')
                self.launcher()
