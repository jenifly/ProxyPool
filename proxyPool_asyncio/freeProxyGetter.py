import asyncio
import re

import aiohttp
from fake_useragent import FakeUserAgentError, UserAgent

from .setting import GET_PROXYPAGE_TIMEOUT

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name != 'FreeProxyGetter':
            attrs['CrawlFunc'] = []
            for k in attrs.keys():
                if 'crawl_' in k:
                    attrs['CrawlFunc'].append(k)
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(metaclass=ProxyMetaclass):

    async def get_raw_proxies(self, callback):
        proxies = await eval("self.{}()".format(callback))
        if proxies is None:
            print(callback, 'is invalid')
            return None
        print('Getting', proxies, 'from', callback)
        return proxies

    
    @staticmethod
    async def get_proxies(urls=None, pattern=None):
        try:
            ua = UserAgent()
        except FakeUserAgentError:
            pass
        tasks = [asyncio.create_task(FreeProxyGetter._fetch(url, {
            'User-Agent':  ua.random,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }, pattern)) for url in urls]
        await asyncio.wait(tasks)
        adress_ports = []
        for task in tasks:
            if task.result() is None:
                return None
            for adress_port in task.result():
                adress_ports.append(':'.join(adress_port))
        return adress_ports

    @staticmethod
    async def _fetch(url, headers, pattern):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=GET_PROXYPAGE_TIMEOUT) as response:
                    return re.findall(pattern, await response.text())
        except:
            pass
