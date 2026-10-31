#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把筛选条件拼成招聘平台的搜索地址（只生成链接，不抓取、不登录）。

用法：
    python boss_url.py --city 重庆 --salary 405 --scale 305 --stage 807 --query 薪酬绩效主管
    python boss_url.py --list

设计说明：
- 只用公开的 URL 参数，不做任何请求。打开链接仍由人自己点。
- 平台随时可能改参数，`--list` 打出来的字典以实测为准，过期了自己改。
- 不要改地址栏里的其他参数，容易被判定为非正常访问。
"""
import argparse
import urllib.parse

BASE = "https://www.zhipin.com/web/geek/jobs"

# 实测值（2026-10）。平台改版后自行更新。
SALARY = {
    "不限": None,
    "3K以下": "402",
    "3-5K": "403",
    "5-10K": "404",
    "10-20K": "405",
    "20-50K": "406",
    "50K以上": "407",
}

SCALE = {
    "不限": None,
    "0-20人": "301",
    "20-99人": "302",
    "100-499人": "303",
    "500-999人": "304",
    "1000-9999人": "305",
    "10000人以上": "306",
}

STAGE = {
    "不限": None,
    "未融资": "801",
    "天使轮": "802",
    "A轮": "803",
    "B轮": "804",
    "C轮": "805",
    "D轮及以上": "806",
    "已上市": "807",
    "不需要融资": "808",
}

CITY = {
    "全国": "100010000",
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280100",
    "深圳": "101280600",
    "杭州": "101210100",
    "成都": "101270100",
    "重庆": "101040100",
    "武汉": "101200100",
    "西安": "101110100",
    "苏州": "101190400",
    "长沙": "101250100",
    "郑州": "101180100",
    "天津": "101030100",
    "南京": "101190100",
}


def resolve(table, value):
    """接受中文名或直接给数字码。"""
    if value is None:
        return None
    if value in table:
        return table[value]
    if str(value).isdigit():
        return str(value)
    raise SystemExit(f"未知取值：{value}（可用值：{', '.join(k for k in table if k != '不限')}）")


def build(city=None, salary=None, scale=None, stage=None, query=None):
    params = {}
    c = resolve(CITY, city)
    if c:
        params["city"] = c
    s = resolve(SALARY, salary)
    if s:
        params["salary"] = s
    sc = resolve(SCALE, scale)
    if sc:
        params["scale"] = sc
    st = resolve(STAGE, stage)
    if st:
        params["stage"] = st
    if query:
        params["query"] = query
    return BASE + ("?" + urllib.parse.urlencode(params) if params else "")


def main():
    ap = argparse.ArgumentParser(description="生成招聘平台搜索链接（不抓取，只拼参数）")
    ap.add_argument("--city")
    ap.add_argument("--salary")
    ap.add_argument("--scale")
    ap.add_argument("--stage")
    ap.add_argument("--query")
    ap.add_argument("--list", action="store_true", help="打印可用的参数取值")
    a = ap.parse_args()

    if a.list:
        for name, table in (("城市", CITY), ("薪资", SALARY), ("规模", SCALE), ("融资阶段", STAGE)):
            print(f"[{name}] " + " | ".join(f"{k}={v}" for k, v in table.items() if v))
        return

    print(build(a.city, a.salary, a.scale, a.stage, a.query))


if __name__ == "__main__":
    main()
