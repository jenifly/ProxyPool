import random

from .db import conn
from .freeProxyGetter import FreeProxyGetter
from .validityTester import ValidityTester


class ResourceDepletionError(Exception):
    def __str__(self):
        return repr('The proxy source is exhausted')


class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        return conn.queue_len >= self._threshold

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            random.shuffle(self._crawler.CrawlFunc)
            for callback in self._crawler.CrawlFunc:
                raw_proxies = self._crawler.get_raw_proxies(callback)
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test_proxies()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError
