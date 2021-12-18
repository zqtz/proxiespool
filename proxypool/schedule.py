try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
import asyncio
import aiohttp
from asyncio import TimeoutError
from multiprocessing import Process
import time
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError,PoolEmptyError
from proxypool.getter import FreeproxiesSpider
from proxypool.setting import *

class ValidityTester(object):
    test_api = TEST_API
    def __init__(self):
        self._raw_proxies = None

    # 定义一个代理函数
    def set_raw_proxies(self,proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()


    async def test_single_proxy(self,proxy):
        # 测试代理,如果有效则放进代理池
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)) as session:
                try:
                    # 判断代理是否为字节类型
                    if isinstance(proxy,bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://'+proxy
                    print('Testing',proxy)
                    # 协程异步对代理进行检查
                    async with session.get(url=self.test_api,proxy=real_proxy,timeout=get_proxy_timeout) as resp:
                        if resp.status == 200:
                            self._conn.put(proxy)
                            print('Vaild_proxy',proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invaild proxy',proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError)as s:
            print(s)
            pass

    # 定义一个异步测试函数
    def test(self):
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except:
            print('ASYNC ERROR')

# 定义一个加代理进代理池的类
class Addpool(object):
    def __init__(self,threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._crawler = FreeproxiesSpider()
        self._tester = ValidityTester()

    # 判断代理长度是否大于设置的最高上限
    def is_over_threshold(self):
        if self._conn.queue_len >= self._threshold:
            return True
        return False

    def add_to_queeu(self):
        print('Addpool is running')
        proxy_count = 0
        # 如果代理的长度小于指定的长度则启动爬虫函数加入代理
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__SpiderFuncCount__):
                callback = self._crawler.__SpiderFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough please waitting to be used')

            if proxy_count == 0:
                raise ResourceDepletionError

class Schedule(object):
    @staticmethod
    # 定时检查代理代理是否有效
    def vaild_proxy(cycle=VALID_CHECK_CYCLE):
        conn = RedisClient()
        tester = ValidityTester()
        while True:
            print('Refreshing ip')
            # count为代理池的一半长度
            count = int(0.5 * conn.queue_len)
            if count == 0:
                print('waitting for add')
                time.sleep(cycle)
                continue
            proxies = conn.get(count)
            tester.set_raw_proxies(proxies)
            tester.test()
            time.sleep(cycle)

    # 如果代理数量小于设定的最低下限则启动add_to_queue加入代理,如果大于等于最高上限则等待代理使用后,数量小于指定上限再加入
    @staticmethod
    def check_pool(upper_threshold=POOL_UPPER_THRESHOLD,
                   lower_threshold=POOL_LOWER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE
                   ):
        conn = RedisClient()
        adder = Addpool(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queeu()
            time.sleep(cycle)

    # 定义多进程同时启动vaild_proxy,check_pool
    def run(self):
        print('IP process is running')
        vaild_process = Process(target=Schedule.vaild_proxy)
        check_process = Process(target=Schedule.check_pool)
        check_process.start()
        vaild_process.start()
