import requests
from bs4 import BeautifulSoup

def get_proxies():
    url = 'http://127.0.0.1:5000/get'
    resp = requests.get(url)
    proxy = BeautifulSoup(resp.text,"lxml").get_text()
    return proxy

def spider(proxy):
    test_url = 'https://dormousehole.readthedocs.io/en/latest/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    proxies = {'http': proxy}
    resp = requests.get(test_url,proxies=proxies,headers=headers)
    return resp.text

def main():
    proxy = get_proxies()
    html = spider(proxy)
    print(html)

if __name__ == '__main__':
    main()

# import os
# import sys
# import requests
# from bs4 import BeautifulSoup
#
# # dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # sys.path.insert(0, dir)
#
#
# def get_proxy():
#     r = requests.get('http://127.0.0.1:5000/get')
#     proxy = BeautifulSoup(r.text, "lxml").get_text()
#     return proxy
#
#
# def crawl(url, proxy):
#     proxies = {'http': proxy}
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
#     }
#     r = requests.get(url, proxies=proxies,headers=headers)
#     return r.text
#
#
# def main():
#     proxy = get_proxy()
#     html = crawl('https://dormousehole.readthedocs.io/en/latest/', proxy)
#     print(html)
#
# if __name__ == '__main__':
#     main()



