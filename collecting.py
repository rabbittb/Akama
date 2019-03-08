#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: liangzhibang@baidu.com
# Date: 2018-09-17

__author__ = "liangzhibang@baidu.com"
__date__ = '2018/9/17'

import asyncio

import Collector
import pybloom

filter = pybloom.BloomFilter(10000)
retval = []


def got_result(future):
    for url in future.result():
        if url not in filter:
            filter.add(url)
            retval.append(url)


def main(keyword:str):
    """
    测试函数，测试抓取bing搜索引擎的性能。
    Collector.bing.fetch(future, "Powered by ASPCMS V2", str(i)) 其中的aspcms是你要搜索的关键字
    目前bing引擎有问题，需要带上cookie访问才能抓取到正确结果。
    所以，目前需要修改Common.py中headers，打开chrome，复制cookie，并覆盖原cookie
    :return:
    """
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(1, 102, 10):
        future = asyncio.Future()
        tasks.append(asyncio.ensure_future(Collector.bing.fetch(future, "keyword", str(i))))
        future.add_done_callback(got_result)
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()