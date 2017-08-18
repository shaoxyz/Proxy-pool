# -*- coding:utf-8 -*-
# Python3
# File    : getsocks.py
# Time    : 2017/8/14 12:16
# Author  : shaweb
import pickle
import time
from pprint import pprint

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
    通过gatherproxy.com下载6000+个socks代理，对小项目来说足够多了。
    :return: a set
    """
    """
    如果不是确定已经登陆 直接请求下载会返回一个页面,"oops!"
    如果已登陆，网页会重定向到infos
    """
    login = host + '/subscribe/login'
    try:
        tmp = session.get(login, timeout=20).text
        html = etree.HTML(tmp)
    except Exception as e:
        print('Login page load failed', 'reason:'.format(e))
        return None, 'Login page load failed'
    try:
        captcha = html.xpath('//*[@id="body"]/form/div[6]/span/text()')[0]
    except:  # captcha = []说明已经是登陆的状态，没有这个标签
        proxies = session.post('http://www.gatherproxy.com/sockslist/plaintext').text
        new = set(proxies.replace('\n', '').split('\r'))
        print('update ', len(new), ' proxies')
        with open('socks.pickle', 'wb') as f:
            pickle.dump(new, f, protocol=pickle.HIGHEST_PROTOCOL)
        return new, None
    else:  # 如果没有报错，说明需要登录
        answer = crack(captcha)
        data = {
            'Username': 'hoimi0922@gmail.com',
            'Password': 'P{SX-cv_',  # 0.0自己去注册一个吧
            'Captcha': answer,
        }
        try:
            session.post(login, data=data)
            return get_socks()
        except:
            return None, 'Login failed'


if __name__ == '__main__':
    proxies, err = get_socks()
    print(proxies, err)
