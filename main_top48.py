import logging
import os
import shutil
import time
import logging
import openpyxl
import pandas as pd

from TraceTool import iTrace
from aw import SeaOfStarsAW
import wda
from aw import ElementNotFoundError

from cases.PerformanceDynamic_Alipay_0010 import PerformanceDynamic_Alipay_0010
from cases.PerformanceDynamic_Alipay_0020 import PerformanceDynamic_Alipay_0020
from cases.PerformanceDynamic_Alipay_0070 import PerformanceDynamic_Alipay_0070
from cases.PerformanceDynamic_AutoNavi_0010 import PerformanceDynamic_AutoNavi_0010
from cases.PerformanceDynamic_AutoNavi_0030 import PerformanceDynamic_AutoNavi_0030
from cases.PerformanceDynamic_AutoNavi_0040 import PerformanceDynamic_AutoNavi_0040
from cases.PerformanceDynamic_AutoNavi_0050 import PerformanceDynamic_AutoNavi_0050
from cases.PerformanceDynamic_AutoNavi_0060 import PerformanceDynamic_AutoNavi_0060
from cases.PerformanceDynamic_baidu_0010 import PerformanceDynamic_baidu_0010
from cases.PerformanceDynamic_baidumap_0010 import PerformanceDynamic_baidumap_0010
from cases.PerformanceDynamic_bilibili_0020 import PerformanceDynamic_bilibili_0020
from cases.PerformanceDynamic_bilibili_0030 import PerformanceDynamic_bilibili_0030
from cases.PerformanceDynamic_bilibili_0040 import PerformanceDynamic_bilibili_0040
from cases.PerformanceDynamic_bilibili_0050 import PerformanceDynamic_bilibili_0050

from cases.PerformanceDynamic_Douyin_0010 import PerformanceDynamic_Douyin_0010
from cases.PerformanceDynamic_Douyin_0030 import PerformanceDynamic_Douyin_0030
from cases.PerformanceDynamic_Douyin_0040 import PerformanceDynamic_Douyin_0040
from cases.PerformanceDynamic_Douyin_0050 import PerformanceDynamic_Douyin_0050
from cases.PerformanceDynamic_fanqie_0010 import PerformanceDynamic_fanqie_0010
from cases.PerformanceDynamic_fanqie_0020 import PerformanceDynamic_fanqie_0020
from cases.PerformanceDynamic_HappyAnimal_0010 import PerformanceDynamic_HappyAnimal_0010
from cases.PerformanceDynamic_hepingjingying_0030 import PerformanceDynamic_hepingjingying_0030
from cases.PerformanceDynamic_jrtt_0010 import PerformanceDynamic_jrtt_0010
from cases.PerformanceDynamic_jrtt_0020 import PerformanceDynamic_jrtt_0020
from cases.PerformanceDynamic_Kuaishou_0010 import PerformanceDynamic_Kuaishou_0010
from cases.PerformanceDynamic_Kuaishou_0020 import PerformanceDynamic_Kuaishou_0020
from cases.PerformanceDynamic_meituan_0010 import PerformanceDynamic_meituan_0010

from cases.PerformanceDynamic_pinduoduo_0010 import PerformanceDynamic_pinduoduo_0010
from cases.PerformanceDynamic_qimao_0010 import PerformanceDynamic_qimao_0010
from cases.PerformanceDynamic_qimao_0020 import PerformanceDynamic_qimao_0020
from cases.PerformanceDynamic_qiyi_0030 import PerformanceDynamic_qiyi_0030

from cases.PerformanceDynamic_Weibo_0020 import PerformanceDynamic_Weibo_0020
from cases.PerformanceDynamic_Weibo_0030 import PerformanceDynamic_Weibo_0030
from cases.PerformanceDynamic_Weibo_0040 import PerformanceDynamic_Weibo_0040
from cases.PerformanceDynamic_weipinhui_0010 import PerformanceDynamic_weipinhui_0010
from cases.PerformanceDynamic_weipinhui_0030 import PerformanceDynamic_weipinhui_0030
from cases.PerformanceDynamic_wpsoffice_0010 import PerformanceDynamic_wpsoffice_0010
from cases.PerformanceDynamic_wpsoffice_0020 import PerformanceDynamic_wpsoffice_0020
from cases.PerformanceDynamic_xhs_0010 import PerformanceDynamic_xhs_0010
from cases.PerformanceDynamic_xhs_0020 import PerformanceDynamic_xhs_0020
from cases.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030
from cases.PerformanceDynamic_xianyu_0010 import PerformanceDynamic_xianyu_0010
from cases.PerformanceDynamic_xianyu_0020 import PerformanceDynamic_xianyu_0020
from cases.PerformanceDynamic_xiechengTrip_0010 import PerformanceDynamic_xiechengTrip_0010
from cases.PerformanceDynamic_xiechengTrip_0020 import PerformanceDynamic_xiechengTrip_0020
from cases.PerformanceDynamic_youku_0020 import PerformanceDynamic_youku_0020
from cases.PerformanceDynamic_zhihu_0030 import PerformanceDynamic_zhihu_0030
from cases.PerformanceDynamic_zuoyebang_0010 import PerformanceDynamic_zuoyebang_0010
from cases.PerformanceDynamic_zuoyebang_0020 import PerformanceDynamic_zuoyebang_0020
from cases.PerformanceDynamic_CloudFlashPay_0010 import PerformanceDynamic_CloudFlashPay_0010
from cases.PerformanceDynamic_Dingding_0010 import PerformanceDynamic_Dingding_0010
from cases.PerformanceDynamic_Dingding_0020 import PerformanceDynamic_Dingding_0020
from cases.PerformanceDynamic_Dongchedi_0010 import PerformanceDynamic_Dongchedi_0010
from cases.PerformanceDynamic_TencentVideo_0010 import PerformanceDynamic_TencentVideo_0010
from cases.PerformanceDynamic_UC_0010 import PerformanceDynamic_UC_0010
from cases.PerformanceDynamic_UC_0020 import PerformanceDynamic_UC_0020
from cases.PerformanceDynamic_jingdong_0010 import PerformanceDynamic_jingdong_0010
from cases.PerformanceDynamic_jingdong_0020 import PerformanceDynamic_jingdong_0020
from cases.PerformanceDynamic_jingdong_0030 import PerformanceDynamic_jingdong_0030
from cases.PerformanceDynamic_jingdong_0040 import PerformanceDynamic_jingdong_0040
from cases.PerformanceDynamic_meituan_0080 import PerformanceDynamic_meituan_0080
from cases.PerformanceDynamic_meituan_0090 import PerformanceDynamic_meituan_0090
from cases.PerformanceDynamic_meituxiuxiu_0010 import PerformanceDynamic_meituxiuxiu_0010
from cases.PerformanceDynamic_qq_0010 import PerformanceDynamic_qq_0010
from cases.PerformanceDynamic_qq_0020 import PerformanceDynamic_qq_0020
from cases.PerformanceDynamic_qqliulanqi_0010 import PerformanceDynamic_qqliulanqi_0010
from cases.PerformanceDynamic_qqm_0010 import PerformanceDynamic_qqm_0010
from cases.PerformanceDynamic_qunaer_0010 import PerformanceDynamic_qunaer_0010
from cases.PerformanceDynamic_qunaer_0020 import PerformanceDynamic_qunaer_0020
from cases.PerformanceDynamic_taobao_0010 import PerformanceDynamic_taobao_0010
from cases.PerformanceDynamic_taobao_0020 import PerformanceDynamic_taobao_0020
from cases.PerformanceDynamic_tencentnews_0010 import PerformanceDynamic_tencentnews_0010
from cases.PerformanceDynamic_ths_0040 import PerformanceDynamic_ths_0040
from cases.PerformanceDynamic_ths_0050 import PerformanceDynamic_ths_0050
from cases.PerformanceDynamic_tielu12306_0010 import PerformanceDynamic_tielu12306_0010
from cases.PerformanceDynamic_tielu12306_0020 import PerformanceDynamic_tielu12306_0020
from cases.PerformanceDynamic_wangzherongyao_0030 import PerformanceDynamic_wangzherongyao_0030
from cases.PerformanceDynamic_weixin_0070 import PerformanceDynamic_weixin_0070
from cases.PerformanceDynamic_weixin_0080 import PerformanceDynamic_weixin_0080
from cases.PerformanceDynamic_weixin_0090 import PerformanceDynamic_weixin_0090
from cases.PerformanceDynamic_weixin_0100 import PerformanceDynamic_weixin_0100
from cases.PerformanceDynamic_weixin_0110 import PerformanceDynamic_weixin_0110
from cases.PerformanceDynamic_xhs_0050 import PerformanceDynamic_xhs_0050
from cases.PerformanceDynamic_AutoNavi_0070 import PerformanceDynamic_AutoNavi_0070
from cases.PerformanceDynamic_AutoNavi_0080 import PerformanceDynamic_AutoNavi_0080
from cases.PerformanceDynamic_Douyin_0020 import PerformanceDynamic_Douyin_0020
from cases.PerformanceDynamic_Douyin_0060 import PerformanceDynamic_Douyin_0060
from cases.PerformanceDynamic_Douyin_0070 import PerformanceDynamic_Douyin_0070
from cases.PerformanceDynamic_Douyin_0080 import PerformanceDynamic_Douyin_0080
from cases.PerformanceDynamic_Douyin_0090 import PerformanceDynamic_Douyin_0090
from cases.PerformanceDynamic_Douyinjisu_0010 import PerformanceDynamic_Douyinjisu_0010
from cases.PerformanceDynamic_MiHome_0010 import PerformanceDynamic_MiHome_0010
from cases.PerformanceDynamic_cloudmusic_0010 import PerformanceDynamic_cloudmusic_0010
from cases.PerformanceDynamic_dazhongdianping_0010 import PerformanceDynamic_dazhongdianping_0010
from cases.PerformanceDynamic_dazhongdianping_0020 import PerformanceDynamic_dazhongdianping_0020
from cases.PerformanceDynamic_deepseek_0010 import PerformanceDynamic_deepseek_0010
from cases.PerformanceDynamic_didichuxing_0020 import PerformanceDynamic_didichuxing_0020
from cases.PerformanceDynamic_doubao_0010 import PerformanceDynamic_doubao_0010
from cases.PerformanceDynamic_doubao_0020 import PerformanceDynamic_doubao_0020
from cases.PerformanceDynamic_eggparty_0010 import PerformanceDynamic_eggparty_0010
from cases.PerformanceDynamic_fanqiechangting_0010 import PerformanceDynamic_fanqiechangting_0010
from cases.PerformanceDynamic_fuzai import PerformanceDynamic_fuzai
from cases.PerformanceDynamic_hongguomianfeiduanju_0010 import PerformanceDynamic_hongguomianfeiduanju_0010
from cases.PerformanceDynamic_hongguomianfeiduanju_0020 import PerformanceDynamic_hongguomianfeiduanju_0020
from cases.PerformanceDynamic_huaweiHealth_0010 import PerformanceDynamic_huaweiHealth_0010
from cases.PerformanceDynamic_huaweiHealth_0020 import PerformanceDynamic_huaweiHealth_0020
from cases.PerformanceDynamic_hwvmall_0010 import PerformanceDynamic_hwvmall_0010
from cases.PerformanceDynamic_hwvmall_0020 import PerformanceDynamic_hwvmall_0020
from cases.PerformanceDynamic_momo_0010 import PerformanceDynamic_momo_0010
from cases.PerformanceDynamic_qianwen_0010 import PerformanceDynamic_qianwen_0010
from cases.PerformanceDynamic_qqm_0040 import PerformanceDynamic_qqm_0040
from cases.PerformanceDynamic_qqm_0050 import PerformanceDynamic_qqm_0050
from cases.PerformanceDynamic_sodamusic_0010 import PerformanceDynamic_sodamusic_0010
from cases.PerformanceDynamic_taptap_0010 import PerformanceDynamic_taptap_0010
from cases.PerformanceDynamic_weixin_0010 import PerformanceDynamic_weixin_0010
from cases.PerformanceDynamic_weixin_0020 import PerformanceDynamic_weixin_0020
from cases.PerformanceDynamic_weixin_0030 import PerformanceDynamic_weixin_0030
from cases.PerformanceDynamic_weixin_0040 import PerformanceDynamic_weixin_0040
from cases.PerformanceDynamic_weixin_0050 import PerformanceDynamic_weixin_0050
from cases.PerformanceDynamic_weixin_0060 import PerformanceDynamic_weixin_0060
from cases.PerformanceDynamic_weixin_0120 import PerformanceDynamic_weixin_0120
from cases.PerformanceDynamic_weixin_0130 import PerformanceDynamic_weixin_0130
from cases.PerformanceDynamic_weixin_0140 import PerformanceDynamic_weixin_0140
from cases.PerformanceDynamic_weixin_0150 import PerformanceDynamic_weixin_0150
from cases.PerformanceDynamic_weixin_0160 import PerformanceDynamic_weixin_0160
from cases.PerformanceDynamic_weixin_0170 import PerformanceDynamic_weixin_0170
from cases.PerformanceDynamic_weixin_0180 import PerformanceDynamic_weixin_0180
from cases.PerformanceDynamic_weixin_0190 import PerformanceDynamic_weixin_0190
from cases.PerformanceDynamic_weixin_0200 import PerformanceDynamic_weixin_0200
from cases.PerformanceDynamic_yuanbao_0010 import PerformanceDynamic_yuanbao_0010


Result_Dir_Path = os.path.join(os.getcwd(), 'Result', time.strftime("%Y%m%d_%H%M%S", time.localtime()))
if os.path.exists(Result_Dir_Path):
    shutil.rmtree(Result_Dir_Path)

os.makedirs(Result_Dir_Path)

# 配置log
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('matplotlib.font_manager').disabled = True
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)
fh = logging.FileHandler(os.path.join(Result_Dir_Path, 'all_log.txt'), encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)


succ_num = 0
fail_num = 0
Basic1 = [
    PerformanceDynamic_fuzai,
    # PerformanceDynamic_fanqie_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_fanqiechangting_0010,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_qianwen_0010,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_hongguomianfeiduanju_0020,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_qq_0020,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Douyinjisu_0010,
    # PerformanceDynamic_meituan_0010,
    # PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_bilibili_0040,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_doubao_0010,
    # PerformanceDynamic_jingdong_0040,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_ths_0040,
    # PerformanceDynamic_xianyu_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_AutoNavi_0070,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_pinduoduo_0010,
    # PerformanceDynamic_Douyin_0090,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_meituan_0080,
    # PerformanceDynamic_eggparty_0010,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_momo_0010,
    # PerformanceDynamic_AutoNavi_0080,
    # PerformanceDynamic_jrtt_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_AutoNavi_0060,
    # PerformanceDynamic_xhs_0030,
    # PerformanceDynamic_Douyin_0040,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_hwvmall_0020,
    # PerformanceDynamic_qq_0010,
    # PerformanceDynamic_fanqiechangting_0010,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_Douyinjisu_0010,
    # PerformanceDynamic_wpsoffice_0020,
    # PerformanceDynamic_weipinhui_0030,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_qunaer_0010,
    # PerformanceDynamic_ths_0050,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_jingdong_0010,
    # PerformanceDynamic_taptap_0010,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_Alipay_0020,
    # PerformanceDynamic_Weibo_0030,
    # PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_hongguomianfeiduanju_0010,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_bilibili_0030,
    # PerformanceDynamic_Weibo_0020,
    # PerformanceDynamic_pinduoduo_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_yuanbao_0010,
    # PerformanceDynamic_tencentnews_0010,
    # PerformanceDynamic_weixin_0150,
    # PerformanceDynamic_taobao_0010,
    # PerformanceDynamic_zuoyebang_0010,
    # PerformanceDynamic_Kuaishou_0010,
    # PerformanceDynamic_weixin_0170,
    # PerformanceDynamic_CloudFlashPay_0010,
    # PerformanceDynamic_baidu_0010,
    # PerformanceDynamic_weixin_0140,
    # PerformanceDynamic_fanqiechangting_0010,
    # PerformanceDynamic_Douyinjisu_0010,
    # PerformanceDynamic_huaweiHealth_0020,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0190,
]

Basic2 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_MiHome_0010,
    PerformanceDynamic_Dongchedi_0010,
    PerformanceDynamic_MiHome_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_MiHome_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_weipinhui_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_qiyi_0030,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_qiyi_0030,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_xianyu_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_zhihu_0030,
    PerformanceDynamic_UC_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_MiHome_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_doubao_0020,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_zhihu_0030,
    PerformanceDynamic_HappyAnimal_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_Douyin_0080,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_meituan_0090,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_Weibo_0030,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_fanqie_0020,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Alipay_0070,
    PerformanceDynamic_zuoyebang_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_doubao_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_Weibo_0040,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_AutoNavi_0040,
    PerformanceDynamic_Dingding_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_hepingjingying_0030,
]

Basic3 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_Douyin_0060,
    PerformanceDynamic_tencentnews_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_qianwen_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_doubao_0020,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_Dingding_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_HappyAnimal_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_didichuxing_0020,
    PerformanceDynamic_UC_0020,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_Alipay_0020,
    PerformanceDynamic_qimao_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_AutoNavi_0050,
    PerformanceDynamic_qunaer_0020,
    PerformanceDynamic_CloudFlashPay_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_CloudFlashPay_0010,
    PerformanceDynamic_qimao_0020,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_qqm_0040,
    PerformanceDynamic_jingdong_0040,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_AutoNavi_0010,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_jingdong_0030,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_bilibili_0020,
    PerformanceDynamic_qqm_0050,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_TencentVideo_0010,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_Douyin_0050,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_dazhongdianping_0020,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_Dingding_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_xiechengTrip_0020,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_sodamusic_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_huaweiHealth_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_eggparty_0010,
]

Basic4 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_hwvmall_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Dongchedi_0010,
    PerformanceDynamic_tielu12306_0020,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_TencentVideo_0010,
    PerformanceDynamic_jingdong_0020,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_dazhongdianping_0010,
    PerformanceDynamic_Douyin_0020,
    PerformanceDynamic_bilibili_0050,
    PerformanceDynamic_qqm_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_didichuxing_0020,
    PerformanceDynamic_sodamusic_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_wpsoffice_0010,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Douyin_0080,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_bilibili_0040,
    PerformanceDynamic_AutoNavi_0030,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_Douyin_0060,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_Alipay_0070,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_xiechengTrip_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_Douyin_0090,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_Douyin_0020,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_AutoNavi_0060,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_AutoNavi_0070,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_AutoNavi_0080,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0080,
]

Basic5 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_Douyin_0070,
    PerformanceDynamic_AutoNavi_0040,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_meituan_0080,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_Douyin_0050,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Douyin_0080,
    PerformanceDynamic_weixin_0200,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_MiHome_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_xhs_0050,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_doubao_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Weibo_0020,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_ths_0040,
    PerformanceDynamic_Douyinjisu_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_weixin_0200,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_weixin_0010,
]

# Basics = [Basic1, Basic2, Basic3, Basic4, Basic5]

Basic = [
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_huaweiHealth_0010,
    PerformanceDynamic_huaweiHealth_0020,
    PerformanceDynamic_hwvmall_0010,
    PerformanceDynamic_hwvmall_0020,
    PerformanceDynamic_mms_0010,
  
    PerformanceDynamic_qianwen_0010,
    PerformanceDynamic_qqm_0040,  
    PerformanceDynamic_qqm_0050,  
    
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0040,

    # PerformanceDynamic_weixin_0120,

    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_qq_0020,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Douyinjisu_0010,
    # PerformanceDynamic_meituan_0010,
    # PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_bilibili_0040,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_doubao_0010,
    # PerformanceDynamic_jingdong_0040,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_ths_0040,
    # PerformanceDynamic_xianyu_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_AutoNavi_0070,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_pinduoduo_0010,
    # PerformanceDynamic_Douyin_0090,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_meituan_0080,
    # PerformanceDynamic_eggparty_0010,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_momo_0010,
    # PerformanceDynamic_AutoNavi_0080,
    # PerformanceDynamic_jrtt_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_AutoNavi_0060,
    # PerformanceDynamic_xhs_0030,
    # PerformanceDynamic_Douyin_0040,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_hwvmall_0020,
    # PerformanceDynamic_qq_0010,
    # PerformanceDynamic_fanqiechangting_0010,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_Douyinjisu_0010,
    # PerformanceDynamic_wpsoffice_0020,
    # PerformanceDynamic_weipinhui_0030,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_qunaer_0010,
    # PerformanceDynamic_ths_0050,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_jingdong_0010,
    # PerformanceDynamic_taptap_0010,
    # PerformanceDynamic_weixin_0040,
    # PerformanceDynamic_Alipay_0020,
    # PerformanceDynamic_Weibo_0030,
    # PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_hongguomianfeiduanju_0010,
    # PerformanceDynamic_weixin_0120,
    # PerformanceDynamic_bilibili_0030,
    # PerformanceDynamic_Weibo_0020,
    # PerformanceDynamic_pinduoduo_0010,
    # PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_yuanbao_0010,
    # PerformanceDynamic_tencentnews_0010,
    # PerformanceDynamic_weixin_0150,
    # PerformanceDynamic_taobao_0010,
    # PerformanceDynamic_zuoyebang_0010,
    # PerformanceDynamic_Kuaishou_0010,
    # PerformanceDynamic_weixin_0170,
    # PerformanceDynamic_CloudFlashPay_0010,
    # PerformanceDynamic_baidu_0010,
    # PerformanceDynamic_weixin_0140,
    # PerformanceDynamic_fanqiechangting_0010,
    # PerformanceDynamic_Douyinjisu_0010,

    # PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0190,
]
Basics = [Basic]

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    result_dict = {'case_name':[],'success':[]}
    SeaOfStarsAW.init_device()
    SeaOfStarsAW.start_trace_thread()
    try:
        for _ in range(1):
            for Basic in Basics:
                for single_case in Basic:
                    try:
                        case = single_case(Result_Dir_Path)
                        result_dict['case_name'].append(case)
                        case.set_up()
                        case.run_case()
                        time.sleep(3)

                        succ_num += 1
                        result_dict['success'].append('1')
                    except ElementNotFoundError as e:
                        logging.error(e)
                        result_dict['success'].append('0')
                        fail_num += 1
                        time.sleep(5)
                        SeaOfStarsAW.stop_trace()
                    except TypeError:
                        result_dict['success'].append('0')
                        time.sleep(5)
                        case = single_case(Result_Dir_Path)
                        case.set_up()
                        case.run_case()
                    except Exception as err:
                        result_dict['success'].append('0')
                        logging.error(err)
                        fail_num += 1
                        time.sleep(5)
                        SeaOfStarsAW.stop_trace()
                    finally:
                        try:
                            SeaOfStarsAW.ut_device.home()
                        except Exception as home_err:
                            logging.error('用例清理时返回主屏幕失败: %s', home_err)
                        #SeaOfStarsAW.swipe_to_launcher()
                        #SeaOfStarsAW.go_home()
                        df = pd.DataFrame(result_dict)
                        df.to_excel(os.path.join(Result_Dir_Path,'result.xlsx'), index=False)
                        pass

    finally:
        logging.info('succ_num - ' + str(succ_num))
        logging.info('fail_num - ' + str(fail_num))
