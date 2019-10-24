from proxyPool_asyncio.poxyPool import PoxyPool
from proxyPool_asyncio.freeProxyGetter import FreeProxyGetter


class MyFreeProxyGetter(FreeProxyGetter):
    async def crawl_kuaidaili(self):
        return await self.get_proxies(['https://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 2)], r'<td data-title="IP">([\d\.]+?)</td>\s*<td data-title="PORT">(\w+)</td>')

    async def crawl_xicidaili(self):
        return await self.get_proxies(['http://www.xicidaili.com/wt/{}'.format(page) for page in range(1, 3)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

    async def crawl_66ip(self):
        return await self.get_proxies(['http://www.66ip.cn/{}.html'.format(page) for page in range(1, 5)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

    async def crawl_kxdaili(self):
        return await self.get_proxies(['http://www.kxdaili.com/dailiip/1/{}.html'.format(page) for page in range(1, 4)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

if __name__ == "__main__":
    PoxyPool.start(MyFreeProxyGetter)