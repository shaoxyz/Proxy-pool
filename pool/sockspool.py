# -*- coding:utf-8 -*-
# Python3
# File    : sockspool
# Time    : 2017/8/16 14:24
# Author  : Shaweb

import requests

socks = ['hk01.ssfvpn.com:1080',
         'hk02.ssfvpn.com:1080',
         'hk03.ssfvpn.com:1080',
         'jp01.ssfvpn.com:1080',
         'jp02.ssfvpn.com:1080',
         'jp03.ssfvpn.com:1080',
         'jp04.ssfvpn.com:1080',
         'jp05.ssfvpn.com:1080',
         'sg01.ssfvpn.com:1080',
         'sg02.ssfvpn.com:1080',
         'sg03.ssfvpn.com:1080',
         'us01.ssfvpn.com:1080',
         'us02.ssfvpn.com:1080',
         'us03.ssfvpn.com:1080',
         'us04.ssfvpn.com:1080',
         'us05.ssfvpn.com:1080']

for proxy in socks:
    proxies = {'http': 'socks5://' + proxy,
               'https': 'socks5://' + proxy}
    r = requests.get('https://www.baidu.com/', proxies=proxies).text
    print(r)
