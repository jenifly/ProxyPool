import asyncio
import re

import aiohttp
from fake_useragent import FakeUserAgentError, UserAgent

from setting import GET_PROXYPAGE_TIMEOUT


async def _fetch(url, headers, pattern):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=GET_PROXYPAGE_TIMEOUT) as response:
                return re.findall(pattern, await response.text())
    except:
        pass


def get_proxies(urls=None, pattern=None):
    loop = asyncio.get_event_loop()
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    tasks = [loop.create_task(_fetch(url, {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }, pattern)) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        for adress_port in task.result():
            yield ':'.join(adress_port)
