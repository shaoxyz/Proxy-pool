"""
关于如何使用该代理池的小爬虫示例。
前提是开启代理池服务，python app.py
"""
# -*- coding:utf-8 -*-
# Python3
# File    : usage.py
# Time    : 2017/8/16 17:39
# Author  : Shaweb

import requests


def select_proxies(selection='socks'):
    if selection == 'socks':
        proxy = requests.get('http://localhost:5000/socks/').text
        # proxy = '127.0.0.1:1080'
        proxies = {'http': 'socks5://' + proxy,
                   'https': 'socks5://' + proxy}
        return proxies
    elif selection == 'https':
        proxy = requests.get('http://localhost:5000/https/').text
        # proxy = '127.0.0.1:1080'
        proxies = {'http': 'http://' + proxy,
                   'https': 'http://' + proxy}
        return proxies
    else:
        raise KeyError


# 先取一个
session = requests.session()
session.proxies.update(select_proxies())


class ProxyPoolUsage(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/subject/26363254/comments?status=P'
        """
            ...
        """

    def crawler(self, selection='socks'):
        try:
            r = session.get(self.url, timeout=10)
        except:
            print('proxy failed！')
            if selection == 'socks':
                proxies = select_proxies()
            elif selection == 'https':
                proxies = select_proxies(selection)
            else:
                raise KeyError
            print('try', proxies)
            session.proxies.update(proxies)
            return self.crawler()
        else:
            if r.status_code == 200:
                print(r, 'Using proxy：', session.proxies, 'Success')
                return self.crawler()
            else:
                print(r.status_code)
                return 'Error'


if __name__ == '__main__':
    ProxyPoolUsage().crawler()


"""
Select https output:

proxies fucked！
try {'http': 'http://175.42.102.252:8118', 'https': 'http://175.42.102.252:8118'}
proxies fucked！
try {'http': 'http://190.206.135.165:8080', 'https': 'http://190.206.135.165:8080'}
proxies fucked！
try {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'}
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
<Response [200]> 使用代理： {'http': 'http://103.217.238.36:53281', 'https': 'http://103.217.238.36:53281'} 成功
...
===========================================
Select socks output:

<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
<Response [200]> 使用代理： {'http': 'socks5://186.204.177.103:65000', 'https': 'socks5://186.204.177.103:65000'} 成功
...
"""


