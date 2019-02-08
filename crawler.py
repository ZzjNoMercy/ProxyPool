# -*- coding:utf-8 -*-

# 获取模块

import json
import requests
from lxml import etree
import time
from proxypool.setting import *


class ProxyMetaclass(type):
    # 定义元类动态获取所有的crawl方法
    def __new__(cls, name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if "crawl_" in k:
                attrs['__CrawlFunc__'].append(k)
                count +=1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass = ProxyMetaclass):
    # 将所有的以crawl开头的方法调用一遍，获取每个方法返回的代理并组合成列表形式返回
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理',proxy)
            proxies.append(proxy)
        return proxies

    # def crawl_kuaidaili(self,page_num = 2):
    #     # 快代理
    #     start_url = 'https://www.kuaidaili.com/free/inha/{}/'
    #     urls = [start_url.format(page) for page in range(1,page_num +1)]
    #     for url in urls:
    #         print('Crawling',url)
    #         r = requests.get(url,headers = headers)
    #         time.sleep(1)
    #         html = etree.HTML(r.text)
    #         trs = html.xpath('//table[@class="table table-bordered table-striped"]//tr')[1:]
    #         for tr in trs:
    #             ip = tr.xpath('.//td[1]/text()')[0]
    #             port = tr.xpath('.//td[2]/text()')[0]
    #             yield ":".join([ip,port])

    def crawl_zhimadaili(self):
        # 芝麻代理
        url = "http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="
        r = requests.get(url)
        result = json.loads(r.text)
        proxies = result.get('data')
        for proxy in proxies:
            ip = proxy.get('ip')
            port = proxy.get('port')
            yield ":".join([ip, str(port)])






