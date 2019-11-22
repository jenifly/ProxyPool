import re

from proxyPool.poxyPool import PoxyPool
from proxyPool.freeProxyGetter import FreeProxyGetter


class MyFreeProxyGetter(FreeProxyGetter):
    async def crawl_kuaidaili(self):
        return await self.get_proxies(
            [f'https://www.kuaidaili.com/free/inha/{page}/' for page in range(1, 2)],
            re.compile(r'<td data-title="IP">([\d\.]+?)</td>\s*<td data-title="PORT">(\w+)</td>'))

    async def crawl_xicidaili(self):
        return await self.get_proxies(
            [f'http://www.xicidaili.com/wt/{page}/' for page in range(1, 3)],
            re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>'))

    async def crawl_66ip(self):
        return await self.get_proxies(
            [f'http://www.66ip.cn/{page}.html' for page in range(1, 5)],
            re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>'))

    async def crawl_kxdaili(self):
        return await self.get_proxies(
            [f'http://www.kxdaili.com/dailiip/1/{page}.html' for page in range(1, 4)],
            re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>'))


if __name__ == "__main__":
    PoxyPool.start(MyFreeProxyGetter)