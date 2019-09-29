from utils import get_proxies


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['CrawlFunc'] = []
        for k in attrs.keys():
            if 'crawl_' in k:
                attrs['CrawlFunc'].append(k)
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = [proxy for proxy in eval("self.{}()".format(callback))]
        print('Getting', proxies, 'from', callback)
        return proxies

    def crawl_kuaidaili(self):
        yield from get_proxies(['https://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 2)], r'<td data-title="IP">([\d\.]+?)</td>\s*<td data-title="PORT">(\w+)</td>')

    def crawl_xicidaili(self):
        yield from get_proxies(['http://www.xicidaili.com/wt/{}'.format(page) for page in range(1, 3)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

    def crawl_66ip(self):
        yield from get_proxies(['http://www.66ip.cn/{}.html'.format(page) for page in range(1, 5)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

    def crawl_kxdaili(self):
        yield from get_proxies(['http://www.kxdaili.com/dailiip/1/{}.html'.format(page) for page in range(1, 4)], r'<td>([\d\.]+?)</td>\s*<td>(\d+?)</td>')

if __name__ == "__main__":
    """
    test crawl
    """
    f = FreeProxyGetter()
    print([x for x in f.crawl_kxdaili()])