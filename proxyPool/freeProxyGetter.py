from .utils import get_proxies

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name != 'FreeProxyGetter':
            attrs['CrawlFunc'] = []
            for k in attrs.keys():
                if 'crawl_' in k:
                    attrs['CrawlFunc'].append(k)
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(metaclass=ProxyMetaclass):
    @staticmethod
    def get_proxies(*kw):
        return get_proxies(*kw)

    def get_raw_proxies(self, callback):
        proxies = [proxy for proxy in eval("self.{}()".format(callback))]
        print('Getting', proxies, 'from', callback)
        return proxies