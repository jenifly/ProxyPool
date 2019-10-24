基于asyncio、aiohttp、uvloop实现的并发代理池，具有简洁、高效、易扩展等特点。同步访问redis队列，实现伪原子性。

## How to use
```python
  
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
```

继承`FreeProxyGetter`类，实现`async def crawl_xxx()`方法，方法名必须为`crawl_`前缀。`self.get_proxies()`接受两个参数，第一个为代理网页url的容器序列类型，第二个为正则表达式。

在asyncio版本中，因所有方法都在一个事件循环中运行，在代理池上限设置的比较高时，可能会造成某些系统（如windows）`select`资源耗尽而抛出异常使得程序中断。对此，请使用`asyncio.Semaphore`限制并发量。

在浏览器中访问`http://127.0.0.1:2345/get`即可获取可用代理。

也可重写`poxyPool.py`中`PoxyPool`类的`web`的类方法实现自定义。伪代码：
```python
from aiohttp import web

@classmethod
def web(slef):
    app = web.Application()
    async def get_proxy(request):
        return web.Response(text=str(conn.pop()))

    async def get_counts(request):
        return web.Response(text=str(conn.queue_len))

    app.add_routes([web.get('/get', get_proxy), web.get('/count', get_counts)])
    return app

```