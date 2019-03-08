#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import asyncio

import Collector
import pybloom
from g import g
from FileScan import start

filter = pybloom.BloomFilter(10000)
retval = []

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}


def got_result(future):
    for url in future.result():
        if url not in filter:
            filter.add(url)
            retval.append(url)


async def main():
    """
    测试函数，测试抓取bing搜索引擎的性能。
    Collector.bing.fetch(future, "Powered by ASPCMS V2", str(i)) 其中的aspcms是你要搜索的关键字
    目前bing引擎有问题，需要带上cookie访问才能抓取到正确结果。
    所以，目前需要修改Common.py中headers，打开chrome，复制cookie，并覆盖原cookie
    :return:
    """
    tasks = []
    for i in range(1, 102, 10):
        tasks.append(asyncio.create_task(Collector.bing.fetch("Powered by ASPCMS V2", str(i))))
    done, pending = await asyncio.wait(tasks)
    tasks = []
    for i in done:
        for item in i.result():
            if item not in filter:
                # tasks.append(asyncio.create_task(start(item)))
                # filter.add(item)
                print(item)
    # await asyncio.wait(tasks)



if __name__ == '__main__':
    g['semaphore'] = asyncio.Semaphore(200)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
