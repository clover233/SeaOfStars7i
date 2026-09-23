import json
import logging
import os
import signal
import shutil
import subprocess
import time
from http.client import RemoteDisconnected
from urllib.request import urlopen
import openpyxl
import pandas as pd

from TraceTool import iTrace
from aw import SeaOfStarsAW
import wda
from aw import ElementNotFoundError

from cases.PerformanceDynamic_alipay_0010 import PerformanceDynamic_alipay_0010
from cases.PerformanceDynamic_alipay_0020 import PerformanceDynamic_alipay_0020
from cases.PerformanceDynamic_alipay_0070 import PerformanceDynamic_alipay_0070
from cases.PerformanceDynamic_autonavi_0010 import PerformanceDynamic_autonavi_0010
from cases.PerformanceDynamic_autonavi_0030 import PerformanceDynamic_autonavi_0030
from cases.PerformanceDynamic_autonavi_0040 import PerformanceDynamic_autonavi_0040
from cases.PerformanceDynamic_autonavi_0050 import PerformanceDynamic_autonavi_0050
from cases.PerformanceDynamic_autonavi_0060 import PerformanceDynamic_autonavi_0060
from cases.PerformanceDynamic_baidu_0010 import PerformanceDynamic_baidu_0010
from cases.PerformanceDynamic_baidumap_0010 import PerformanceDynamic_baidumap_0010
from cases.PerformanceDynamic_beiwanglu_0010 import PerformanceDynamic_beiwanglu_0010
from cases.PerformanceDynamic_beiwanglu_0020 import PerformanceDynamic_beiwanglu_0020
from cases.PerformanceDynamic_bilibili_0020 import PerformanceDynamic_bilibili_0020
from cases.PerformanceDynamic_bilibili_0030 import PerformanceDynamic_bilibili_0030
from cases.PerformanceDynamic_bilibili_0040 import PerformanceDynamic_bilibili_0040
from cases.PerformanceDynamic_bilibili_0050 import PerformanceDynamic_bilibili_0050
from cases.PerformanceDynamic_call_0010 import PerformanceDynamic_call_0010
from cases.PerformanceDynamic_call_0020 import PerformanceDynamic_call_0020
from cases.PerformanceDynamic_camera_0020 import PerformanceDynamic_camera_0020
from cases.PerformanceDynamic_camera_0030 import PerformanceDynamic_camera_0030
from cases.PerformanceDynamic_douyin_0010 import PerformanceDynamic_douyin_0010
from cases.PerformanceDynamic_douyin_0030 import PerformanceDynamic_douyin_0030
from cases.PerformanceDynamic_douyin_0040 import PerformanceDynamic_douyin_0040
from cases.PerformanceDynamic_douyin_0050 import PerformanceDynamic_douyin_0050
from cases.PerformanceDynamic_fanqie_0010 import PerformanceDynamic_fanqie_0010
from cases.PerformanceDynamic_fanqie_0020 import PerformanceDynamic_fanqie_0020
from cases.PerformanceDynamic_happyanimal_0010 import PerformanceDynamic_happyanimal_0010
from cases.PerformanceDynamic_hepingjingying_0030 import PerformanceDynamic_hepingjingying_0030
from cases.PerformanceDynamic_jrtt_0010 import PerformanceDynamic_jrtt_0010
from cases.PerformanceDynamic_jrtt_0020 import PerformanceDynamic_jrtt_0020
from cases.PerformanceDynamic_kuaishou_0010 import PerformanceDynamic_kuaishou_0010
from cases.PerformanceDynamic_kuaishou_0020 import PerformanceDynamic_kuaishou_0020
from cases.PerformanceDynamic_meituan_0010 import PerformanceDynamic_meituan_0010
from cases.PerformanceDynamic_pinduoduo_0010 import PerformanceDynamic_pinduoduo_0010
from cases.PerformanceDynamic_qimao_0010 import PerformanceDynamic_qimao_0010
from cases.PerformanceDynamic_qimao_0020 import PerformanceDynamic_qimao_0020
from cases.PerformanceDynamic_qiyi_0030 import PerformanceDynamic_qiyi_0030
from cases.PerformanceDynamic_weibo_0020 import PerformanceDynamic_weibo_0020
from cases.PerformanceDynamic_weibo_0030 import PerformanceDynamic_weibo_0030
from cases.PerformanceDynamic_weibo_0040 import PerformanceDynamic_weibo_0040
from cases.PerformanceDynamic_weipinhui_0010 import PerformanceDynamic_weipinhui_0010
from cases.PerformanceDynamic_weipinhui_0030 import PerformanceDynamic_weipinhui_0030
from cases.PerformanceDynamic_wpsoffice_0010 import PerformanceDynamic_wpsoffice_0010
from cases.PerformanceDynamic_wpsoffice_0020 import PerformanceDynamic_wpsoffice_0020
from cases.PerformanceDynamic_xhs_0010 import PerformanceDynamic_xhs_0010
from cases.PerformanceDynamic_xhs_0020 import PerformanceDynamic_xhs_0020
from cases.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030
from cases.PerformanceDynamic_xianyu_0010 import PerformanceDynamic_xianyu_0010
from cases.PerformanceDynamic_xiechengtrip_0010 import PerformanceDynamic_xiechengtrip_0010
from cases.PerformanceDynamic_xiechengtrip_0020 import PerformanceDynamic_xiechengtrip_0020
from cases.PerformanceDynamic_youku_0020 import PerformanceDynamic_youku_0020
from cases.PerformanceDynamic_zhihu_0030 import PerformanceDynamic_zhihu_0030
from cases.PerformanceDynamic_zuoyebang_0010 import PerformanceDynamic_zuoyebang_0010
from cases.PerformanceDynamic_zuoyebang_0020 import PerformanceDynamic_zuoyebang_0020
from cases.PerformanceDynamic_cloudflashpay_0010 import PerformanceDynamic_cloudflashpay_0010
from cases.PerformanceDynamic_dingding_0010 import PerformanceDynamic_dingding_0010
from cases.PerformanceDynamic_dingding_0020 import PerformanceDynamic_dingding_0020
from cases.PerformanceDynamic_dongchedi_0010 import PerformanceDynamic_dongchedi_0010
from cases.PerformanceDynamic_tencentvideo_0010 import PerformanceDynamic_tencentvideo_0010
from cases.PerformanceDynamic_uc_0010 import PerformanceDynamic_uc_0010
from cases.PerformanceDynamic_uc_0020 import PerformanceDynamic_uc_0020
from cases.PerformanceDynamic_jingdong_0010 import PerformanceDynamic_jingdong_0010
from cases.PerformanceDynamic_jingdong_0020 import PerformanceDynamic_jingdong_0020
from cases.PerformanceDynamic_jingdong_0030 import PerformanceDynamic_jingdong_0030
from cases.PerformanceDynamic_jingdong_0040 import PerformanceDynamic_jingdong_0040
from cases.PerformanceDynamic_meituan_0080 import PerformanceDynamic_meituan_0080
from cases.PerformanceDynamic_meituan_0090 import PerformanceDynamic_meituan_0090
from cases.PerformanceDynamic_meituxiuxiu_0010 import PerformanceDynamic_meituxiuxiu_0010
from cases.PerformanceDynamic_photo_0010 import PerformanceDynamic_photo_0010
from cases.PerformanceDynamic_photo_0030 import PerformanceDynamic_photo_0030
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
from cases.PerformanceDynamic_autonavi_0070 import PerformanceDynamic_autonavi_0070
from cases.PerformanceDynamic_autonavi_0080 import PerformanceDynamic_autonavi_0080
from cases.PerformanceDynamic_douyin_0020 import PerformanceDynamic_douyin_0020
from cases.PerformanceDynamic_douyin_0060 import PerformanceDynamic_douyin_0060
from cases.PerformanceDynamic_douyin_0070 import PerformanceDynamic_douyin_0070
from cases.PerformanceDynamic_douyin_0080 import PerformanceDynamic_douyin_0080
from cases.PerformanceDynamic_douyin_0090 import PerformanceDynamic_douyin_0090
from cases.PerformanceDynamic_douyinjisu_0010 import PerformanceDynamic_douyinjisu_0010
from cases.PerformanceDynamic_mihome_0010 import PerformanceDynamic_mihome_0010
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
from cases.PerformanceDynamic_huaweihealth_0010 import PerformanceDynamic_huaweihealth_0010
from cases.PerformanceDynamic_huaweihealth_0020 import PerformanceDynamic_huaweihealth_0020
from cases.PerformanceDynamic_hwvmall_0010 import PerformanceDynamic_hwvmall_0010
from cases.PerformanceDynamic_hwvmall_0020 import PerformanceDynamic_hwvmall_0020
from cases.PerformanceDynamic_momo_0010 import PerformanceDynamic_momo_0010
from cases.PerformanceDynamic_qianwen_0010 import PerformanceDynamic_qianwen_0010
from cases.PerformanceDynamic_qqm_0040 import PerformanceDynamic_qqm_0040
from cases.PerformanceDynamic_qqm_0050 import PerformanceDynamic_qqm_0050
from cases.PerformanceDynamic_sodamusic_0010 import PerformanceDynamic_sodamusic_0010
from cases.PerformanceDynamic_taptap_0010 import PerformanceDynamic_taptap_0010
from cases.PerformanceDynamic_weather_0010 import PerformanceDynamic_weather_0010
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
logging.getLogger('PIL').setLevel(logging.WARNING)
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
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_qianwen_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_douyin_0030,
    PerformanceDynamic_bilibili_0040,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_doubao_0010,
    PerformanceDynamic_jingdong_0040,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_ths_0040,
    PerformanceDynamic_xianyu_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_camera_0020,
    PerformanceDynamic_weather_0010,
    PerformanceDynamic_autonavi_0070,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_douyin_0090,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_meituan_0080,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_autonavi_0080,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_call_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_autonavi_0060,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_douyin_0040,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_hwvmall_0020,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_call_0020,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_wpsoffice_0020,
    PerformanceDynamic_weipinhui_0030,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_qunaer_0010,
    PerformanceDynamic_ths_0050,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_photo_0030,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_jingdong_0010,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_alipay_0020,
    PerformanceDynamic_weibo_0030,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_bilibili_0030,
    PerformanceDynamic_weibo_0020,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_douyin_0030,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_tencentnews_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_zuoyebang_0010,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_cloudflashpay_0010,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_huaweihealth_0020,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0190,
]

Basic2 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_mihome_0010,
    PerformanceDynamic_dongchedi_0010,
    PerformanceDynamic_mihome_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_mihome_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_douyin_0040,
    PerformanceDynamic_weipinhui_0010,
    PerformanceDynamic_douyinjisu_0010,
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
    PerformanceDynamic_uc_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_mihome_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_doubao_0020,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_zhihu_0030,
    PerformanceDynamic_happyanimal_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_photo_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_douyin_0030,
    PerformanceDynamic_douyin_0080,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_meituan_0090,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_weibo_0030,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_fanqie_0020,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_alipay_0070,
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
    PerformanceDynamic_douyin_0040,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_kuaishou_0020,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_weibo_0040,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_autonavi_0040,
    PerformanceDynamic_dingding_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_hepingjingying_0030,
]

Basic3 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_douyin_0060,
    PerformanceDynamic_tencentnews_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_qianwen_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_doubao_0020,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_dingding_0020,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_happyanimal_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_didichuxing_0020,
    PerformanceDynamic_uc_0020,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_douyin_0030,
    PerformanceDynamic_alipay_0020,
    PerformanceDynamic_qimao_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_autonavi_0050,
    PerformanceDynamic_qunaer_0020,
    PerformanceDynamic_cloudflashpay_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_weather_0010,
    PerformanceDynamic_cloudflashpay_0010,
    PerformanceDynamic_qimao_0020,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_qqm_0040,
    PerformanceDynamic_jingdong_0040,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_autonavi_0010,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_jingdong_0030,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_bilibili_0020,
    PerformanceDynamic_qqm_0050,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_tencentvideo_0010,
    PerformanceDynamic_momo_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_douyin_0050,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_dazhongdianping_0020,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_dingding_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_xiechengtrip_0020,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_sodamusic_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_huaweihealth_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_kuaishou_0020,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_eggparty_0010,
]

Basic4 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_douyin_0040,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_hwvmall_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_dongchedi_0010,
    PerformanceDynamic_tielu12306_0020,
    PerformanceDynamic_photo_0030,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_tencentvideo_0010,
    PerformanceDynamic_jingdong_0020,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_dazhongdianping_0010,
    PerformanceDynamic_douyin_0020,
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
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_douyin_0080,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_bilibili_0040,
    PerformanceDynamic_autonavi_0030,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_douyin_0060,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_kuaishou_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_alipay_0070,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_camera_0020,
    PerformanceDynamic_xiechengtrip_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_photo_0010,
    PerformanceDynamic_douyin_0030,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_call_0010,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_douyin_0090,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_call_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_douyin_0020,
    PerformanceDynamic_call_0010,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_autonavi_0060,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_call_0020,
    PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_autonavi_0070,
    PerformanceDynamic_call_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_call_0020,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_autonavi_0080,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0080,
]

Basic5 = [
    PerformanceDynamic_fuzai,
    PerformanceDynamic_douyin_0070,
    PerformanceDynamic_autonavi_0040,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_alipay_0010,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_meituan_0080,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_photo_0030,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_cloudmusic_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_douyin_0050,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_fanqiechangting_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_call_0010,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_weixin_0140,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_weixin_0190,
    PerformanceDynamic_deepseek_0010,
    PerformanceDynamic_call_0020,
    PerformanceDynamic_weixin_0010,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_douyin_0040,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_kuaishou_0010,
    PerformanceDynamic_weixin_0040,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_douyin_0080,
    PerformanceDynamic_weixin_0200,
    PerformanceDynamic_eggparty_0010,
    PerformanceDynamic_mihome_0010,
    PerformanceDynamic_weixin_0120,
    PerformanceDynamic_hongguomianfeiduanju_0020,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_taptap_0010,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_xhs_0050,
    PerformanceDynamic_hongguomianfeiduanju_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_camera_0030,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_yuanbao_0010,
    PerformanceDynamic_weixin_0130,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0180,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0150,
    PerformanceDynamic_weixin_0170,
    PerformanceDynamic_doubao_0010,
    PerformanceDynamic_beiwanglu_0020,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weibo_0020,
    PerformanceDynamic_weixin_0160,
    PerformanceDynamic_beiwanglu_0010,
    PerformanceDynamic_weixin_0060,
    PerformanceDynamic_ths_0040,
    PerformanceDynamic_douyinjisu_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_douyin_0010,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_douyin_0010,
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

Basics = [Basic3]

WDA_STATUS_URL = 'http://127.0.0.1:8100/status'
WDA_RECOVERY_TIMEOUT_SECONDS = 600
WDA_RECOVERY_POLL_SECONDS = 3


def wda_ready():
    """与 supervisor 使用相同的 /status 就绪条件。"""
    try:
        with urlopen(WDA_STATUS_URL, timeout=3) as response:
            if response.status != 200:
                return False
            status = json.load(response)
            value = status.get('value') if isinstance(status, dict) else None
            return isinstance(value, dict) and value.get('ready') is True
    except (OSError, ValueError, TypeError):
        return False


def wait_for_wda_recovery(aw, timeout=WDA_RECOVERY_TIMEOUT_SECONDS):
    """等待 supervisor 重建 WDA，并确认新设备连接可以返回桌面。"""
    logging.warning('等待 WDA 恢复，最长 %s 秒', timeout)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if wda_ready():
            try:
                aw.init_device()
                aw.ut_device.home()
            except Exception as error:
                logging.warning('WDA 状态已就绪，但设备操作仍失败：%s', error)
            else:
                logging.info('WDA 已恢复，继续执行后续用例')
                return True
        time.sleep(min(WDA_RECOVERY_POLL_SECONDS,
                       max(0, deadline - time.monotonic())))
    logging.error('等待 WDA 恢复超过 %s 秒，本批次剩余用例停止执行', timeout)
    return False

def wda_connection_lost(error):
    """识别 WDA 传输中断；业务层的 WDA 错误仍按用例失败处理。"""
    current = error
    while current is not None:
        if isinstance(current, (ConnectionRefusedError, ConnectionResetError,
                                BrokenPipeError, RemoteDisconnected)):
            return True
        current = current.__cause__ or current.__context__
    return False


def cleanup_case(aw, return_home=True):
    trace_stopped = True
    try:
        if aw.trace_thread is not None:
            aw.stop_trace()
    except Exception:
        trace_stopped = False
        logging.exception('停止 trace 失败')

    if not return_home:
        return trace_stopped, True

    for attempt in range(1, 4):
        try:
            aw.ut_device.home()
            return trace_stopped, False
        except Exception as error:
            if wda_connection_lost(error):
                logging.error('WDA 连接已中断，返回桌面失败：%s', error)
                return False, True
            if attempt < 3:
                time.sleep(2)
            else:
                logging.error('WDA 返回桌面失败（重试 3 次）：%s', error)
    return False, False


def run_cases(case_groups, result_dir, aw, results):
    for group in case_groups:
        for case_class in group:
            started_at = time.monotonic()
            case = None
            success = '0'
            disconnected = False
            try:
                case = case_class(result_dir)
                case.set_up()
                case.run_case()
                success = '1'
            except AssertionError:
                logging.error('用例 %s 执行失败，当前步骤：%s',
                              case_class.__name__,
                              getattr(case, 'current_step', '初始化/准备环境'))
            except Exception as error:
                disconnected = wda_connection_lost(error)
                if disconnected:
                    logging.error('WDA 连接已中断，用例 %s 停在步骤 %s：%s',
                                  case_class.__name__,
                                  getattr(case, 'current_step', '初始化/准备环境'),
                                  error)
                else:
                    logging.exception('用例 %s 执行失败，当前步骤：%s',
                                      case_class.__name__,
                                      getattr(case, 'current_step', '初始化/准备环境'))
            finally:
                cleanup_ok, cleanup_disconnected = cleanup_case(
                    aw, return_home=not disconnected)
                disconnected = disconnected or cleanup_disconnected
                if not cleanup_ok:
                    success = '0'
                    if not disconnected:
                        logging.error('用例 %s 收尾失败', case_class.__name__)
                results['case_name'].append(case_class.__name__)
                results['success'].append(success)
                try:
                    pd.DataFrame(results).to_excel(
                        os.path.join(result_dir, 'result.xlsx'), index=False)
                except Exception:
                    logging.exception(
                        '结果保存失败，结果仍保留在内存中，下个用例结束后再次尝试保存')
            logging.info('用例 %s 执行耗时 %.1f 秒，结果 %s',
                         case_class.__name__, time.monotonic() - started_at,
                         '成功' if success == '1' else '失败')
            if disconnected and not wait_for_wda_recovery(aw):
                return

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 启动内存采集脚本
    mem_script_path = os.path.join(os.path.dirname(__file__), 'mem', 'memcollct.sh')
    mem_process = subprocess.Popen(['bash', mem_script_path],
                                   start_new_session=True)
    logging.info(f'Memory collection started with PID: {mem_process.pid}')

    result_dict = {'case_name':[],'success':[]}
    try:
        SeaOfStarsAW.init_device()
        SeaOfStarsAW.start_trace_thread()
        run_cases(Basics, Result_Dir_Path, SeaOfStarsAW, result_dict)

    finally:
        succ_num = result_dict['success'].count('1')
        fail_num = result_dict['success'].count('0')
        logging.info('succ_num - ' + str(succ_num))
        logging.info('fail_num - ' + str(fail_num))
        stop_result = subprocess.run(['bash', mem_script_path, 'stop'],
                                     capture_output=True,
                                     text=True)
        if stop_result.returncode != 0:
            logging.error('Failed to stop memory collection: %s', stop_result.stderr.strip())
        try:
            mem_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(mem_process.pid, signal.SIGTERM)
            mem_process.wait(timeout=5)
        logging.info('Memory collection stopped')
