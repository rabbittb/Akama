#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: liangzhibang@baidu.com
# Date: 2018-09-06
import asyncio
import logging
import random
from urllib.parse import urlparse
from aiohttp import ClientSession

import aiohttp

from g import g

__author__ = "liangzhibang@baidu.com"
__date__ = '2018/9/6'

urls_cache = {}
timeout = {}



async def request(url, func, *args, **requests):
    async with g['semaphore']:
        netloc = urlparse(url).netloc
        if netloc in urls_cache:
            session = urls_cache.get(netloc)
        else:
            session = aiohttp.ClientSession()
            urls_cache[netloc] = session

        try:
            # 以2s 为一个周期，尽量将任务都均匀分布在2s内
            await asyncio.sleep(random.uniform(0, 2.0))
            async with session.request(*args, url=url, timeout=5, **requests) as response:
                return await func(url, response)
        except asyncio.TimeoutError:
            return False
        except aiohttp.client_exceptions.ClientConnectorError:
            return False
        except aiohttp.client_exceptions.ClientOSError:
            return False


async def _request(url, func, *args, **requests):
    async with g['semaphore']:
        try:
            await asyncio.sleep(random.uniform(0, 2.0))
            async with ClientSession() as session:
                async with session.get(*args, url=url, timeout=5, **requests) as response:
                    return await func(url, response)
        except asyncio.TimeoutError:
            return False
        except aiohttp.client_exceptions.ClientConnectorError:
            return False
        except aiohttp.client_exceptions.ClientOSError:
            return False
        except Exception:
            return False


async def session_closed(url):
    netloc = urlparse(url).netloc
    if netloc in urls_cache:
        session = urls_cache.get(netloc)
        await session.close()
        del urls_cache[netloc]


def get_logger():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    formatter.datefmt = DATE_FORMAT
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger = logging.getLogger('asyncio')
    logger.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    # logger.addHandler(ch)

    return logger
