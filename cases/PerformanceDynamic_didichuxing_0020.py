from aw import SeaOfStarsAW
from cases.didi_common import DidiCase


class PerformanceDynamic_didichuxing_0020(DidiCase):
    """Excel 7.0.2：浏览滴滴个人中心、出行服务、搜索和车主服务。"""

    @SeaOfStarsAW.function_log
    def run_case(self):
        for iteration in range(self.TEST_TIME):
            with self.capture_trace(iteration, 1):
                self.step(1, '启动滴滴出行')
                self.start_didi()
            self.step(2, '点击我的')
            self.open_my()
            self.step(3, '点击钱包')
            self.open_wallet()
            self.step(4, '返回我的界面')
            self.return_wallet_to_my()
            self.step(5, '点击订单后返回我的界面')
            self.open_my_item_and_return('全部订单')
            self.step(6, '点击设置后返回我的界面')
            self.open_my_item_and_return('设置')
            self.step(7, '点击底部首页图标，回到首页')
            self.return_home()
            self.step(8, '点击城际拼车后返回首页')
            self.open_home_service_and_return('城际拼车')
            self.step(9, '点击顺风车后返回首页')
            self.open_home_service_and_return('顺风车')
            self.step(10, '点击打车后返回首页')
            self.open_home_service_and_return('打车')
            self.step(11, '点击青桔骑行后返回首页')
            self.open_home_service_and_return('青桔骑行')
            self.step(12, '点击搜索框')
            self.open_destination_search()
            self.step(13, '输入大雁塔北广场南停车场')
            self.enter_destination('大雁塔北广场南停车场')
            self.step(14, '浏览搜索结果，上滑2次，下滑2次')
            self.browse_destination_results(2, 2)
            self.step(15, '返回滴滴出行首页')
            self.return_home()
            self.step(16, '点击车主')
            self.open_owner()
            self.step(17, '点击特惠洗车并浏览，上滑5次，下滑5次')
            self.open_owner_feature('特惠洗车')
            self.browse(5, 5)
            self.step(18, '点击看车选车并浏览，上滑5次，下滑5次')
            self.return_owner()
            self.open_owner_more_feature('看车选车')
            self.browse(5, 5)
            self.step(19, '返回滴滴出行主界面')
            self.return_home()
            with self.capture_trace(iteration, 20):
                self.step(20, '滑动返回Home页')
                self.launcher()
