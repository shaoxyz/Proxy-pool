# -*- coding:utf-8 -*-
# Python3
# @File    : gethttps.py
# @Time    : 2017/8/13 22:16
# @Author  : shaweb
"""
从国内各个发布免费代理的网站抓代理
"""

import re
import pickle
import requests
from bs4 import BeautifulSoup

from utils import errorCatch

class GetFreeProxy(object):
    """
    http(s) proxy getter
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    def __init__(self):
        pass

    @staticmethod
    @errorCatch
    def freeProxyFirst(page=10):
        """
        快代理IP http://www.kuaidaili.com/
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))

        for url in url_list:
            html = requests.get(url, headers=GetFreeProxy.headers).content
            tree = BeautifulSoup(html, 'lxml')
            proxy_list = tree.select('#freelist > table > tbody > tr')
            for proxy in proxy_list:
                # print(proxy)
                ip = proxy.select('td')[0].text
                port = proxy.select('td')[1].text
                x = ip + ':' + port
                yield x

    @staticmethod
    @errorCatch
    def freeProxySecond(proxy_number=50):
        """
        代理66 http://www.66ip.cn/
        """
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)

        html = requests.get(url, headers=GetFreeProxy.headers).text

        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    @staticmethod
    @errorCatch
    def freeProxyThird():
        """
        西刺 http://api.xicidaili.com/free2016.txt
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            html = requests.get(each_url, headers=GetFreeProxy.headers).content
            soup = BeautifulSoup(html, 'lxml')
            proxy_list = soup.find_all('tr')[1:]
            # print(len(proxy_list), proxy_list[1:])
            for proxy in proxy_list:
                ip = proxy.find_all('td')[1].text
                port = proxy.find_all('td')[2].text
                x = ip + ':' + port
                yield x

    @staticmethod
    @errorCatch
    def freeProxyFourth():
        """
        无忧 http://www.data5u.com/
        """
        url_list = ['http://www.data5u.com/',
                    'http://www.data5u.com/free/',
                    'http://www.data5u.com/free/gngn/index.shtml',
                    'http://www.data5u.com/free/gnpt/index.shtml']
        for url in url_list:
            html_tree = requests.get(url, headers=GetFreeProxy.headers).content
            soup = BeautifulSoup(html_tree, 'lxml')
            ul_list = soup.find_all('ul', 'l2')
            for ul in ul_list:
                ip = ul.find_all('span')[0].text
                port = ul.find_all('span')[1].text
                x = ip + ":" + port
                yield x

    @staticmethod
    @errorCatch
    def freeProxyFifth():
        """
        ip181 http://www.ip181.com/
        """
        url = 'http://www.ip181.com/'
        html_tree = requests.get(url, headers=GetFreeProxy.headers).content
        soup = BeautifulSoup(html_tree, 'lxml')
        tr_list = soup.find_all('tr')[1:]
        for tr in tr_list:
            ip = tr.find_all('td')[0].text
            port = tr.find_all('td')[1].text
            x = ip + ":" + port
            yield x


def get_https():
    p = ['freeProxyFirst', 'freeProxySecond', 'freeProxyThird', 'freeProxyFourth', 'freeProxyFifth']
    proxy_set = set()
    for i in p:
        for proxy in getattr(GetFreeProxy, i)():
            proxy_set.add(proxy)
    print('update ', len(proxy_set), ' proxies')
    # _saveIntxt(proxy_set)
    # save_in_redis(proxy_set)
    with open('https.pickle', 'wb') as f:
        pickle.dump(proxy_set, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    get_https()
