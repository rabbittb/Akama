#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import asyncio
import sys
import time

from Common import request, get_logger, session_closed
from g import g

# 设置日志的参数
logger = get_logger()

# windows需要单独设置为iocp，不然无法发挥协程高并发优势
# 具体参照cpython的实现
if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()

suffixes = ['.rar', '.zip', '.sql', '.gz', '.sql.gz', '.tar.gz']
features = ['</web-app>', 'repositoryformatversion', 'svn://']

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}


async def selfscan(url, response):
    """
    更新判断规则
        1. 状态码200
        2. Content-Type在返回头中
        3. Content-Type 不是text/html或image/*
    """
    content_type = response.headers.get('Content-Type')
    if content_type and 'application' in content_type:
        return [url, response.headers.get('Content-Length')]
    return False


async def scan(target_url):
    response = await request(target_url, selfscan, "HEAD", headers=headers, ssl=False)
    if not response:
        return False
    url, size = response
    logger.debug("[*] finded backup file : %s size: %d M" % (url, int(size) // 1024 // 1024))
    return url, size


def get_scanlist_from_url(url: str):
    """
    从url中生成敏感文件待扫描列表
    :param url:
    :return:
    """
    file_dic = ['.git/config', '.svn/entries', 'WEB-INF/web.xml', 'web.rar', 'web.tar.gz', 'wwwroot.gz', 'ftp.rar',
                '__zep__/js.zip', 'flashfxp.rar', 'flashfxp.tar', 'faisunzip.zip', 'ftp.tar.gz',
                'wwwroot.sql', 'www.rar', 'flashfxp.zip', 'ftp.tar', 'data.zip', 'wwwroot.tar', 'www.tar.gz',
                'data.rar', 'admin.rar', 'ftp.zip',
                'web.tar', 'admin.zip', 'www.tar', 'wwwroot.zip', 'admin.tar', 'backup.zip', 'flashfxp.tar.gz',
                'bbs.zip', 'wwwroot.sql.zip',
                'www.zip', 'web.zip', 'wwwroot.rar', 'data.tar', 'admin.tar.gz', 'wwwroot.tar.gz', 'data.tar.gz']

    url = url.replace('http://', '').replace('https://', '')
    host_items = url.split('.')
    for suffix in suffixes:
        file_dic.append("".join(host_items[1:]) + suffix)
        file_dic.append(host_items[1] + suffix)
        file_dic.append(host_items[-2] + suffix)
        file_dic.append("".join(host_items) + suffix)
        file_dic.append(url + suffix)
    return list(set(file_dic))


async def start(url):
    tasks = []
    scanlist = get_scanlist_from_url(url)
    for item in scanlist:
        target_url = url + "/" + item
        task = asyncio.create_task(scan(target_url))
        tasks.append(task)
    await asyncio.wait(tasks)
    await asyncio.wait_for(session_closed(url), timeout=0.1)
    # 清理任务
    # py3.7 不会完全取消协程，需要手动一下
    # 参考 https://mail.python.org/pipermail/python-list/2016-February/702847.html
    return False


def main(url_list):
    loop = asyncio.get_event_loop()
    tasks = []
    for url in url_list:
        task = loop.create_task(start(url))
        tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    # loop = asyncio.ProactorEventLoop()
    # url_list = ['http://www.wszg.org', 'http://www.czsjzq.gov.cn', 'http://www.court.gov.cn']
    url_list = ['http://www.txx111.com/', 'http://www.jqww123.com/', 'http://yzzhu88.com/', 'http://www.qing155.com/',
                'http://www.jsjqqmy.com/', 'http://www.nyl093.com/', 'http://yzjqw00.com/', 'http://zzxs123.com/',
                'http://www.xinkai14.com/', 'http://www.czc8.cn/', 'http://xinkai68.com/', 'http://scyz2.com/',
                'http://www.qmw866.com/', 'http://yzqm55.com/', 'http://www.fswsdj.com/', 'http://nyw188.com/',
                'http://www.nyl004.com/', 'http://wsdp86.com/', 'http://sdy55.com/', 'http://www.emiao143.com/',
                'http://xinn3.com/', 'http://www.miaomu87.com/', 'http://www.nyl19.com/', 'http://miaomu412.com/',
                'http://www.reafonsteel.com/?LanguageAlias1=en', 'http://nyl076.com/', 'http://tshuwai.com/',
                'http://www.qwpr6.com/', 'http://hw066.com/', 'http://www.jszhu118.com/', 'http://xink13.com/',
                'http://www.miaomu82.com/', 'http://www.jsykzy.com/', 'http://shxiaojiang.com/', 'http://xinkai19.com/',
                'http://nyl055.com/', 'http://xingk66.com/', 'http://nlw588.com/', 'http://nyl07.com/',
                'http://www.taidi7.com/', 'http://www.nyyz9.com/', 'http://nyl056.com/', 'http://www.baichenjh.com/',
                'http://www.miaomu06.com/', 'http://xinkai09.com/', 'http://shuichan14.com', 'http://www.kyqyyz.com/',
                'http://jqyz8.com/', 'http://xinkai50.com/', 'http://jqyz1.com/', 'http://www.xmw169.com/',
                'http://xinkai31.com/', 'http://www.zyzhuy.com/', 'http://dgbojuzs.com/', 'http://nyyz899.com/',
                'http://www.qwpr16.com/', 'http://shuichan12.com/', 'http://sdy113.com/', 'http://xinkai22.com/',
                'http://xink666.com/', 'http://jszy055.com/', 'http://lxmyzw.com/', 'http://cadwj.com/',
                'http://shuichan15.com', 'http://www.gxbeyy.com/', 'http://sdy09.com/', 'http://www.snzhuye.com/',
                'http://www.miaomu415.com/', 'http://www.qwpr37.com/', 'http://www.xyjdjdsb.com/',
                'http://wsdp011.com/',
                'http://xinkai62.com/', 'http://www.xinkai80.com/', 'http://nyl063.com/', 'http://www.nyl13.com/',
                'http://www.qmyz55.com/', 'http://www.xkzhuye.com/', 'http://www.diaochezhixiao.com/',
                'http://www.taidi6.com/', 'http://wsdp888.com/', 'http://sdy117.com/', 'http://xinkai65.com/',
                'http://nyl091.com/', 'http://www.nlwjg.com/', 'http://zizhu413.com/', 'http://www.emiao415.com/',
                'http://jy85g.com/', 'http://www.nyl12.com/', 'http://www.wiremeshengineer.com/', 'http://rjy2.com/',
                'http://fcgas.com/', 'http://dzyumiao.com/', 'http://www.qmyz77.com/', 'http://www.nyl66.com/',
                'http://www.jszdjgw.com/', 'http://jszy886.com/', 'http://xink14.com/']
    now = time.time()
    g['semaphore'] = asyncio.Semaphore(500)
    main(url_list)
    print("time usage:\t", time.time() - now)
