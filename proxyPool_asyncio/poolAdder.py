import random

from .db import conn
from .setting import POOL_UPPER_THRESHOLD
from .freeProxyGetter import FreeProxyGetter
from .validityTester import ValidityTester


class ResourceDepletionError(Exception):
    def __str__(self):
        return repr('The proxy source is exhausted')


class PoolAdder(object):

    def __init__(self, crawler, tester):
        self._tester = tester
        self._crawler = crawler()

    def is_over_threshold(self):
        return conn.queue_len >= POOL_UPPER_THRESHOLD

    async def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            random.shuffle(self._crawler.CrawlFunc)
            for callback in self._crawler.CrawlFunc:
                raw_proxies = await self._crawler.get_raw_proxies(callback)
                if raw_proxies is None:
                    continue
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test_proxies()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError
