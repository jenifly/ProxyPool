import asyncio

import aiohttp

from asyncio import TimeoutError

from .db import conn
from .setting import GET_PROXY_TIMEOUT, TEST_API

try:
    from aiohttp.errors import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError


class ValidityTester(object):
    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies

    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(TEST_API, proxy=real_proxy, timeout=GET_PROXY_TIMEOUT) as response:
                        if response.status == 200:
                            conn.put(proxy)
                            print('Valid proxy', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError) as e:
                    print('Invalid proxy', proxy, e)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            print(s)

    def test_proxies(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy)
                     for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except (ValueError, TimeoutError):
            print('Async Error')
