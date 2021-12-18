from .utils import get_page
from lxml import etree
import re
import pyquery as pq


class ProxyMetaclass(type):
    '''
    metaclass为一个元类,FreeproxiesSpider加入了
    __SpiderFunc__,__SpiderFncCount__后,
    获得了爬虫函数和爬虫函数的属性
    '''
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__SpiderFunc__'] = []
        for k,v in attrs.items():
            if 'spider_' in k:
                attrs['__SpiderFunc__'].append(k)
                count += 1
        attrs['__SpiderFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class FreeproxiesSpider(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        # eval()方法执行爬虫函数返回代理
        for proxy in eval(f'self.{callback}()'):
            print('Spiding',proxy, 'from',callback)
            proxies.append(proxy)
        return proxies

    def spider_kuaidaili(self):
        for page in range(1,6):
            spider_url = 'https://www.kuaidaili.com/free/inha/'+str(page)
            html = get_page(spider_url)
            pat = re.compile('<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>')
            results = pat.findall(str(html))
            for host,port in results:
                yield host + ':' + port.replace(' ','')

    def spider_66ip(self):
        for page in range(1, 6):
            spider_url = 'http://www.66ip.cn/' + str(page)+'.html'
            html = get_page(spider_url)
            pat = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>')
            results = pat.findall(str(html))
            for host, port in results:
                yield host + ':' + port.replace(' ','')

    def spider_kxdaili(self):
        for page in range(1, 6):
            spider_url = 'http://www.kxdaili.com/dailiip/1/' + str(page)+'.html'
            html = get_page(spider_url)
            pat = re.compile('<td>(.*?)</td>\s*' +
                             '<td>(.*?)</td>')
            results = pat.findall(pat)
            for host, port in results:
                yield host + ':' + port.replace(' ','')

    def spider_proxylist(self):
        spider_url = 'http://proxylist.fatezero.org/proxy.list'
        html = get_page(spider_url)
        pat = re.compile('"host": "(.*?)", "port":(.*?),')
        results = pat.findall(pat)
        for host, port in results:
            proxy = host + ':' + port
            yield proxy.replace(' ','')



