import asyncio
from Common import _request
from g import g
from urllib.parse import urlparse
import sys, re
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

fuck_list = []


async def Links_scan(url, response):  # 抓取所有 tag a 再判断 url 是否合法
    html = await response.content.read()
    url_list = []
    if html:
        html = BeautifulSoup(html, 'lxml')
        links = list(html.find_all('a'))
        for link in links:
            url = re.findall('href="(.*?)"', str(link), re.S)
            if url and urlparse(url[0]).netloc:
                url = url[0]
                if urlparse(url).scheme == "http" or urlparse(url).scheme == "https":
                    res_url = urlparse(url).scheme + "://" + urlparse(url).netloc
                else:
                    res_url = "http://" + urlparse(url).netloc
                if res_url not in fuck_list:  # 简单的过滤 判断是否重复
                    url_list.append(res_url)
                    fuck_list.append(res_url)
    return url_list


async def Links(url):  # 获取友链
    # TODO FILITER
    res_list = await _request(url, Links_scan)
    return res_list


def main(target_list):  # 无限循环爬取友链测试效果
    res_list, tasks = [], []
    if len(target_list) >= 100:
        target_list = target_list[1:100]  # 任务量太大 取前100个创建任务
    print("本轮开启任务数量", target_list)
    for url in target_list:
        task = loop.create_task(Links(url))
        tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks))
    for task in tasks:
        if task.result():
            res_list = res_list + task.result()
    if res_list:
        print("[*]采集到", len(res_list), res_list)
        return main(res_list)


if __name__ == "__main__":
    g['semaphore'] = asyncio.Semaphore(500)
    loop = asyncio.get_event_loop()
    a = ['https://www.hao123.com/']
    b = ['https://account.shen88.cn', 'https://dashi.shen88.cn', 'https://images.shen88.cn',
         'https://services.shen88.cn', 'https://www.shen88.cn', 'https://xingming.shen88.cn',
         'https://shengxiao.shen88.cn', 'http://www.fengshui55.com', 'http://mengyongcheng.cn',
         'https://www.xilihua.com', 'http://www.zhongguozizhi.com', 'https://www.baimatech.com',
         'http://www.beian.gov.cn']
    main(b)
    # print(len(a))
    # tasks = []
    # for url in a:
    #     task = loop.create_task(Links(url))
    #     tasks.append(task)
    # loop.run_until_complete(asyncio.gather(*tasks))
    # for task in tasks:
    #     if task.result():
    #         print(task.result())
