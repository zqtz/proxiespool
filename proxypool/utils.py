import requests
from requests.exceptions import ConnectionError
from fake_useragent import FakeUserAgent,FakeUserAgentError
import random
import asyncio
import aiohttp


# 定义一个获取网页html函数
def get_page(url,options={}):
    try:
        ua = FakeUserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    print(base_headers)
    headers = dict(base_headers)
    print('Crawling',url)
    try:
        resp = requests.get(url,headers=headers,**options)
        print('Geting result', url, resp.status_code)
        if resp.status_code == 200:
            return resp.text
    except ConnectionError:
        print('Crawl Failed',url)
        return None

class downloader(object):
    '''
    一个异步下载器,请求太频繁,容易被禁止
    '''
    def __init__(self,urls,htmls):
        self._urls = urls
        self._htmls = htmls

    async def download_single_page(self,url):
        async with aiohttp.ClientSession(url) as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text)


    def download_all_page(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self._urls]
        loop.run_until_complete(asyncio.wait(tasks))

    def html(self):
        self.download_all_page()
        return self._htmls




    


