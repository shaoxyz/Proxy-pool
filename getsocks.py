# -*- coding:utf-8 -*-
# Python3
# File    : getsocks.py
# Time    : 2017/8/14 12:16
# Author  : shaweb
"""
墙外的代理网站GatherProxy.com，需要VPN
其验证码..形同虚设..
"""
import pickle
import time
from lxml import etree
from utils import crack
import requests

headers = {
    'Host': 'www.gatherproxy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
proxies = {
    'https': 'http://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
session = requests.session()
session.headers.update(headers)
session.proxies.update(proxies)
host = 'http://www.gatherproxy.com'


def get_socks():
    """
    :return: a set
    """
    login = host + '/subscribe/login'

    try:
        tmp = session.get(login, timeout=20).text
        # print(tmp)
        html = etree.HTML(tmp)
        # print(html)
        captcha = html.xpath('//*[@id="body"]/form/div[6]/span/text()')[0]
    except Exception as e:
        print('GatherProxy.com request failed!', e)
        return None, '--> Request captcha failed.'
    answer = crack(captcha)
    data = {
        'Username': 'hoimi0922@gmail.com',
        'Password': xxx,  # 自己去注册个吧~很方便
        'Captcha': answer,
    }
    try:
        session.post(login, data=data)
    except:
        return None, '--> Login failed.'
    try:
        proxies = session.post('http://www.gatherproxy.com/sockslist/plaintext').text
        new = set(proxies.replace('\n', '').split('\r'))
        print('update ', len(new), ' proxies')
        with open('socks.pickle', 'wb') as f:
            pickle.dump(new, f, protocol=pickle.HIGHEST_PROTOCOL)
        return new, None
    except:
        return None, '--> Download SocksList failed.'


if __name__ == '__main__':
    proxies, err = get_socks()
    print(proxies, err)

