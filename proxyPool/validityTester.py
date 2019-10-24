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
        print('ValidityTester is working')
        try:
            for proxy in self._raw_proxies:
                asyncio.create_task(self.test_single_proxy(proxy))
        except (ValueError, TimeoutError):
            print('Async Error')
