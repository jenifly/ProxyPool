import asyncio

from aiohttp import web

from .db import conn
from .poolAdder import PoolAdder
from .setting import (POOL_LEN_CHECK_CYCLE, POOL_LOWER_THRESHOLD,
                     POOL_UPPER_THRESHOLD, VALID_CHECK_CYCLE, WEB_API_PORT)
from .validityTester import ValidityTester


def Interval_cycle(t):
    def wrapper(func):
        async def inner(*args, **kwargs):
            await func(*args, **kwargs)
            await asyncio.sleep(t)
            asyncio.create_task(inner(*args, **kwargs))
        return inner
    return wrapper


class PoxyPool:
    @staticmethod
    @Interval_cycle(VALID_CHECK_CYCLE)
    async def valid_proxy(tester=None):
        count = int(0.5 * conn.queue_len)
        if count == 0:
            print('Waiting for adding')
            return
        raw_proxies = conn.get(count)
        tester.set_raw_proxies(raw_proxies)
        tester.test_proxies()

    @staticmethod
    @Interval_cycle(POOL_LEN_CHECK_CYCLE)
    async def check_pool(adder=None):
        if conn.queue_len < POOL_UPPER_THRESHOLD:
            await adder.add_to_queue()
    
    @classmethod
    def web(slef):
        app = web.Application()
        async def get_proxy(request):
            return web.Response(text=str(conn.pop()))

        async def get_counts(request):
            return web.Response(text=str(conn.queue_len))

        app.add_routes([web.get('/get', get_proxy), web.get('/count', get_counts)])
        return app

    @classmethod
    def start(cls, proxy_getter=None):
        if proxy_getter == None:
            raise Exception('proxy_getter is not None')
        tester = ValidityTester()
        adder = PoolAdder(proxy_getter, tester)
        loop = asyncio.get_event_loop()
        loop.create_task(cls.check_pool(adder))
        loop.create_task(cls.valid_proxy(tester))
        loop.create_task(web._run_app(cls.web(), port=WEB_API_PORT))
        loop.run_forever()

