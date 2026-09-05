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

from case48.PerformanceDynamic_58city_0010 import PerformanceDynamic_58city_0010
from case48.PerformanceDynamic_58city_0020 import PerformanceDynamic_58city_0020
from case48.PerformanceDynamic_Alipay_0010 import PerformanceDynamic_Alipay_0010
from case48.PerformanceDynamic_Alipay_0020 import PerformanceDynamic_Alipay_0020
from case48.PerformanceDynamic_Alipay_0070 import PerformanceDynamic_Alipay_0070

from case48.PerformanceDynamic_AutoNavi_0010 import PerformanceDynamic_AutoNavi_0010
from case48.PerformanceDynamic_AutoNavi_0030 import PerformanceDynamic_AutoNavi_0030
from case48.PerformanceDynamic_AutoNavi_0040 import PerformanceDynamic_AutoNavi_0040
from case48.PerformanceDynamic_AutoNavi_0050 import PerformanceDynamic_AutoNavi_0050
from case48.PerformanceDynamic_AutoNavi_0060 import PerformanceDynamic_AutoNavi_0060
from case48.PerformanceDynamic_Baidu_0010 import PerformanceDynamic_Baidu_0010
from case48.PerformanceDynamic_Baidumap_0010 import PerformanceDynamic_Baidumap_0010

from case48.PerformanceDynamic_Bilibili_0020 import PerformanceDynamic_Bilibili_0020
from case48.PerformanceDynamic_Bilibili_0030 import PerformanceDynamic_Bilibili_0030
from case48.PerformanceDynamic_Bilibili_0040 import PerformanceDynamic_Bilibili_0040
from case48.PerformanceDynamic_Bilibili_0050 import PerformanceDynamic_Bilibili_0050

from case48.PerformanceDynamic_Dongchedi_0020 import PerformanceDynamic_Dongchedi_0020
from case48.PerformanceDynamic_Douyin_0010 import PerformanceDynamic_Douyin_0010
from case48.PerformanceDynamic_Douyin_0030 import PerformanceDynamic_Douyin_0030
from case48.PerformanceDynamic_Douyin_0040 import PerformanceDynamic_Douyin_0040
from case48.PerformanceDynamic_Douyin_0050 import PerformanceDynamic_Douyin_0050
from case48.PerformanceDynamic_fanqie_0010 import PerformanceDynamic_fanqie_0010
from case48.PerformanceDynamic_fanqie_0020 import PerformanceDynamic_fanqie_0020
from case48.PerformanceDynamic_hanglvzongheng_0010 import PerformanceDynamic_hanglvzongheng_0010
from case48.PerformanceDynamic_hanglvzongheng_0020 import PerformanceDynamic_hanglvzongheng_0020
from case48.PerformanceDynamic_HappyAnimal_0010 import PerformanceDynamic_HappyAnimal_0010
from case48.PerformanceDynamic_hepingjingying_0030 import PerformanceDynamic_hepingjingying_0030
from case48.PerformanceDynamic_jrtt_0010 import PerformanceDynamic_jrtt_0010
from case48.PerformanceDynamic_jrtt_0020 import PerformanceDynamic_jrtt_0020
from case48.PerformanceDynamic_kiwi_0010 import PerformanceDynamic_kiwi_0010
from case48.PerformanceDynamic_kiwi_0020 import PerformanceDynamic_kiwi_0020
from case48.PerformanceDynamic_kiwi_0030 import PerformanceDynamic_kiwi_0030
from case48.PerformanceDynamic_Kuaishou_0010 import PerformanceDynamic_Kuaishou_0010
from case48.PerformanceDynamic_Kuaishou_0020 import PerformanceDynamic_Kuaishou_0020
from case48.PerformanceDynamic_mangguoTV_0010 import PerformanceDynamic_mangguoTV_0010
from case48.PerformanceDynamic_meituan_0010 import PerformanceDynamic_meituan_0010

from case48.PerformanceDynamic_pinduoduo_0010 import PerformanceDynamic_pinduoduo_0010
from case48.PerformanceDynamic_qimao_0010 import PerformanceDynamic_qimao_0010
from case48.PerformanceDynamic_qimao_0020 import PerformanceDynamic_qimao_0020
from case48.PerformanceDynamic_qiyi_0010 import PerformanceDynamic_qiyi_0010
from case48.PerformanceDynamic_qiyi_0020 import PerformanceDynamic_qiyi_0020
from case48.PerformanceDynamic_qiyi_0030 import PerformanceDynamic_qiyi_0030
from case48.PerformanceDynamic_qiyi_0060 import PerformanceDynamic_qiyi_0060
from case48.PerformanceDynamic_qiyi_0070 import PerformanceDynamic_qiyi_0070

from case48.PerformanceDynamic_Weibo_0010 import PerformanceDynamic_Weibo_0010
from case48.PerformanceDynamic_Weibo_0020 import PerformanceDynamic_Weibo_0020
from case48.PerformanceDynamic_Weibo_0030 import PerformanceDynamic_Weibo_0030
from case48.PerformanceDynamic_Weibo_0040 import PerformanceDynamic_Weibo_0040
from case48.PerformanceDynamic_weipinhui_0010 import PerformanceDynamic_weipinhui_0010
from case48.PerformanceDynamic_weipinhui_0020 import PerformanceDynamic_weipinhui_0020
from case48.PerformanceDynamic_weipinhui_0030 import PerformanceDynamic_weipinhui_0030
from case48.PerformanceDynamic_wpsoffice_0010 import PerformanceDynamic_wpsoffice_0010
from case48.PerformanceDynamic_wpsoffice_0020 import PerformanceDynamic_wpsoffice_0020
from case48.PerformanceDynamic_xhs_0010 import PerformanceDynamic_xhs_0010
from case48.PerformanceDynamic_xhs_0020 import PerformanceDynamic_xhs_0020
from case48.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030
from case48.PerformanceDynamic_xhs_0040 import PerformanceDynamic_xhs_0040
from case48.PerformanceDynamic_xianyu_0010 import PerformanceDynamic_xianyu_0010
from case48.PerformanceDynamic_xianyu_0020 import PerformanceDynamic_xianyu_0020
from case48.PerformanceDynamic_xiechengTrip_0010 import PerformanceDynamic_xiechengTrip_0010
from case48.PerformanceDynamic_xiechengTrip_0020 import PerformanceDynamic_xiechengTrip_0020
from case48.PerformanceDynamic_ximalaya_0010 import PerformanceDynamic_ximalaya_0010
from case48.PerformanceDynamic_ximalaya_0020 import PerformanceDynamic_ximalaya_0020
from case48.PerformanceDynamic_xuexiqiangguo_0010 import PerformanceDynamic_xuexiqiangguo_0010
from case48.PerformanceDynamic_xuexiqiangguo_0020 import PerformanceDynamic_xuexiqiangguo_0020
from case48.PerformanceDynamic_youku_0010 import PerformanceDynamic_youku_0010
from case48.PerformanceDynamic_youku_0020 import PerformanceDynamic_youku_0020
from case48.PerformanceDynamic_zhihu_0030 import PerformanceDynamic_zhihu_0030
from case48.PerformanceDynamic_zhongzai_0010 import PerformanceDynamic_zhongzai_0010
from case48.PerformanceDynamic_zhongzai_0020 import PerformanceDynamic_zhongzai_0020
from case48.PerformanceDynamic_zuoyebang_0010 import PerformanceDynamic_zuoyebang_0010
from case48.PerformanceDynamic_zuoyebang_0020 import PerformanceDynamic_zuoyebang_0020






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
PerformanceDynamic_Douyin_0040,
]

Basics=[Basic1]

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
                        SeaOfStarsAW.ut_device.home()
                        #SeaOfStarsAW.swipe_to_launcher()
                        #SeaOfStarsAW.go_home()
                        df = pd.DataFrame(result_dict)
                        df.to_excel(os.path.join(Result_Dir_Path,'result.xlsx'), index=False)
                        pass

    finally:
        logging.info('succ_num - ' + str(succ_num))
        logging.info('fail_num - ' + str(fail_num))
