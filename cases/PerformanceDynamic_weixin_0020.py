from aw import SeaOfStarsAW
from cases.weixin_common import WeixinCase


class PerformanceDynamic_weixin_0020(WeixinCase):
    """Excel 7.0.2：添加朋友、朋友圈评论及九图选择。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            self.prepare_iteration()
            with self.capture_trace_5s(iteration, 1):
                self.step(1, '启动微信')
                self.start_weixin()
            self.finish_weixin_start()
            self.step(2, '点击右上角+号')
            self.tap('快捷操作', max_y=120, wait=1)
            self.step(3, '点击添加朋友，切换到添加朋友页面')
            self.tap('添加朋友', min_y=100, max_y=260, wait=2)
            self.step(4, '点击搜索框，输入好友账号点击查询')
            if not self.FRIEND_ACCOUNT:
                self.fail('请通过 WEIXIN_FRIEND_ACCOUNT 配置要查询的微信号/手机号')
            self.tap('账号/手机号', wait=1)
            self.enter_text(self.FRIEND_ACCOUNT, clear=True)
            self.tap('Search', '搜索', min_y=600, wait=3)
            self.step(5, '返回微信主界面')
            self.return_weixin_home()
            self.step(6, '点击发现，切换到发现页面')
            self.tap('发现', min_y=760, wait=2)
            self.step(7, '点击朋友圈，切换到朋友圈页面')
            self.tap('朋友圈', min_y=90, max_y=220, wait=4)
            self.dismiss_optional_prompts()
            self.step(8, '浏览朋友圈上滑3次，下滑3次')
            self.browse(3, 3)
            self.step(9, '在第一条朋友圈评论真不错')
            self.comment_first_moment('真不错')
            self.step(10, '点击右上角相机按钮')
            self.open_moments_camera_menu()
            self.step(11, '点击拍摄，切换到拍照页面后返回上一页')
            self.tap('拍摄', contains=True, min_y=600, wait=3)
            self.tap('取消', '返回', max_y=160, wait=2)
            self.step(12, '九宫格选择9张照片')
            self.open_moments_camera_menu()
            self.tap('从手机相册选择', min_y=650, wait=3)
            self.select_photos(9)
            self.tap('关闭', '取消', max_y=140, wait=2)
            self.step(13, '返回微信主界面')
            self.return_weixin_home()
            with self.capture_trace_5s(iteration, 14):
                self.step(14, '滑动返回Home页')
                self.launcher()
