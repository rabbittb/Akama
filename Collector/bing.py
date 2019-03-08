#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: liangzhibang@baidu.com
# Date: 2018-09-06

__author__ = "liangzhibang@baidu.com"
__date__ = '2018/9/6'
from selectolax.parser import HTMLParser

from Common import request, session_closed

__all__ = ["fetch"]

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': "DUP=Q=DMF1ucDxtqgxw5niaXcmYQ2&T=337420307&A=2&IG=650049F2DFBC456581C55D0ABE8C48BA; _EDGE_V=1; MUID=28B287D3929A61F5126B8B8A93B460AB; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=6ED0F5D11238447D88D2AF7C764FB99F&dmnchg=1; MUIDB=28B287D3929A61F5126B8B8A93B460AB; BFBN=gRCkFn2abFMUrtdt-CrdGN6v_n5MgtcclUQj3QN_FmzSfw; _EDGE_S=mkt=zh-cn&F=1&SID=3018363887FF6D4013143A6186D16CED; SRCHUSR=DOB=20180828&T=1536565506000; _FP=hta=off; ENSEARCH=BENVER=0; SNRHOP=I=&TS=; ipv6=hit=1536572516779&t=4; _SS=SID=3018363887FF6D4013143A6186D16CED&HV=1536569635&bIm=211394; SRCHHPGUSR=CW=1262&CH=254&DPR=2&UTC=480&WTS=63672165714"
}


async def selfrequest(url, response):
    return await response.text()


async def fetch(keywords: str, first: str) -> list:
    bing_url = "https://www4.bing.com/search?q=%s&first=%s" % (keywords, first)
    content = await request(bing_url, selfrequest, "GET", headers=headers, ssl=False)
    if content:
        response_parser = HTMLParser(content)
        retval = []
        for node in response_parser.css("li.b_algo h2 a"):
            retval.append(node.attributes['href'])
        return retval
    else:
        return None
