#!/usr/bin/env python3
"""Arrange one connected iPhone's SpringBoard pages to match README.md."""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.springboard import SpringBoardServicesService


TARGET_PAGES = [
    [
        "com.tencent.qqchschess",
        "com.zhanlang.swgd66",
        "com.tuyoo.doudizhu.3d",
        "com.7k7k.gouji",
        "com.apple.Passbook",
        "m.qidian.QDReaderAppStore",
        "com.wang.CNRNewMediaApp",
        "com.kugou.kugou1002",
        "com.sina.sinanews",
        "com.tencent.peng",
        "ifengNews",
        "com.sohu.newspaper",
        "com.Qting.QTTour",
        "com.yytingting.iting",
        "yyvoice",
        "com.kiloo.subwaysurf.cn",
    ],
    [
        "com.alipay.iphoneclient",
        "com.autonavi.amap",
        "com.baidu.BaiduMobile",
        "com.baidu.map",
        "com.apple.mobilenotes",
        "tv.danmaku.bilianime",
        "com.apple.mobilephone",
        "com.apple.camera",
        "com.unionpay.chsp",
        "com.netease.cloudmusic",
        "com.dianping.dpscope",
        "com.deepseek.chat",
        "com.ss.iphone.ugc.aweme.lite",
        "com.netease.party",
        "com.xiaomi.mihome",
        "com.wemomo.momoappdemo1",
        "com.easyplay.taptap.now",
        "com.tencent.hunyuan.app.chat",
        "com.xiaojukeji.didi",
        "com.laiwang.DingTalk",
    ],
    [
        "com.ss.ios.auto",
        "com.bot.doubao",
        "com.ss.iphone.ugc.Aweme",
        "com.dragon.read",
        "com.xs.fm",
        "com.happyelements.1OSAnimal",
        "com.tencent.tmgp.pubgmhd",
        "com.phoenix.video",
        "com.huawei.iossporthealth",
        "com.vmall.ios",
        "com.360buy.jdmobile",
        "com.ss.iphone.article.News",
        "com.jiangjia.gif",
        "com.meituan.imeituan",
        "com.meitu.mtxx",
        "com.apple.MobileSMS",
        "com.apple.mobileslideshow",
        "com.xunmeng.pinduoduo",
        "com.aliyun.ios.tongyi",
        "com.yueyou.cyreader",
    ],
    [
        "com.qiyi.iphone",
        "com.tencent.mqq",
        "com.tencent.mttlite",
        "com.tencent.QQMusic",
        "com.qunar.iphoneclient8",
        "com.apple.Preferences",
        "com.soda.music",
        "com.taobao.taobao4iphone",
        "com.tencent.info",
        "com.tencent.live4iphone",
        "cn.com.10jqka.IHexin",
        "cn.12306.rails12306",
        "com.ucweb.iphone.lowversion",
        "com.tencent.smoba",
        "com.apple.weather",
        "com.sina.weibo",
        "com.vipshop.iphone",
        "com.tencent.xin",
        "com.kingsoft.www.office.wpsoffice",
        "com.xingin.discover",
    ],
    [
        "com.taobao.fleamarket",
        "ctrip.com",
        "com.youku.YouKu",
        "com.zhihu.ios",
        "com.baidu.homework",
    ],
]


def walk_icons(value):
    if isinstance(value, dict):
        bundle_id = value.get("bundleIdentifier")
        if bundle_id:
            yield bundle_id, value
        for child in value.values():
            yield from walk_icons(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_icons(child)


def without_targets(value, targets):
    if isinstance(value, dict):
        if value.get("bundleIdentifier") in targets:
            return None
        result = {}
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                filtered = without_targets(child, targets)
                result[key] = [] if filtered is None and isinstance(child, list) else filtered
            else:
                result[key] = child
        return result
    if isinstance(value, list):
        result = []
        for child in value:
            filtered = without_targets(child, targets)
            if filtered is not None:
                result.append(filtered)
        return result
    return value


def page_bundle_ids(page):
    return [item.get("bundleIdentifier") for item in page if item.get("bundleIdentifier")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--udid", required=True)
    parser.add_argument("--backup-dir", type=Path, default=Path("Result/icon_layout_backups"))
    args = parser.parse_args()

    with create_using_usbmux(serial=args.udid) as lockdown:
        service = SpringBoardServicesService(lockdown)
        before = service.get_icon_state()

        args.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = args.backup_dir / f"{args.udid}_{timestamp}.json"
        backup_path.write_text(
            json.dumps(before, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )

        icon_map = {}
        for bundle_id, icon in walk_icons(before):
            icon_map.setdefault(bundle_id, icon)

        all_targets = {bundle_id for page in TARGET_PAGES for bundle_id in page}
        missing = [bundle_id for page in TARGET_PAGES for bundle_id in page if bundle_id not in icon_map]

        dock = without_targets(before[0], all_targets)
        page_one = without_targets(before[1], all_targets)
        trailing_non_targets = []
        for old_page in before[2:]:
            trailing_non_targets.extend(without_targets(old_page, all_targets))

        if trailing_non_targets:
            folder = next((item for item in page_one if item.get("listType") == "folder"), None)
            if folder is None:
                raise RuntimeError("No folder is available on page 1 for non-target overflow icons")
            icon_lists = folder.setdefault("iconLists", [[]])
            if not icon_lists:
                icon_lists.append([])
            icon_lists[0].extend(trailing_non_targets)

        arranged_pages = [
            [copy.deepcopy(icon_map[bundle_id]) for bundle_id in page if bundle_id in icon_map]
            for page in TARGET_PAGES
        ]
        intended = [dock, page_one, *arranged_pages]

        if Counter(bundle_id for bundle_id, _ in walk_icons(before)) != Counter(
            bundle_id for bundle_id, _ in walk_icons(intended)
        ):
            raise RuntimeError("Safety check failed: intended layout would lose or duplicate icons")

        service.set_icon_state(intended)
        after = service.get_icon_state()

    actual_pages = [page_bundle_ids(page) for page in after[2:7]]
    expected_pages = [[bundle_id for bundle_id in page if bundle_id in icon_map] for page in TARGET_PAGES]
    if actual_pages != expected_pages:
        raise RuntimeError(
            "SpringBoard did not retain the requested order:\n"
            f"expected={expected_pages!r}\nactual={actual_pages!r}"
        )

    print(json.dumps({
        "backup": str(backup_path.resolve()),
        "missing": missing,
        "dock_count": len(after[0]),
        "page_counts": [len(page) for page in after[1:]],
        "target_page_bundle_ids": actual_pages,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
