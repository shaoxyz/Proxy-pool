# -*- coding:utf-8 -*-
# Python3
# File    : getsocks.py
# Time    : 2017/8/14 12:16
# Author  : shaweb
import pickle
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

    # 抓验证码, 没抓到就重复抓到为止, 偶尔需要多请求几次
    login = host + '/subscribe/login'
    while True:
        try:
            tmp = session.get(login, timeout=20).text
            # print(tmp)
            html = etree.HTML(tmp)
            # print(html)
            captcha = html.xpath('//*[@id="body"]/form/div[6]/span/text()')[0]
            break
        except:
            print('GatherProxy.com request failed, retry..')
            continue
    answer = crack(captcha)
    data = {
        'Username': 'hoimi0922@gmail.com',
        'Password': yourselfAccount,
        'Captcha': answer,
    }
    try:
        session.post(login, data=data)
    except:
        return None, 'Login failed.'
    try:
        proxies = session.post('http://www.gatherproxy.com/sockslist/plaintext').text
        new = set(proxies.replace('\n', '').split('\r'))
        print('update ', len(new), ' proxies')
        with open('socks.pickle', 'wb') as f:
            pickle.dump(new, f, protocol=pickle.HIGHEST_PROTOCOL)
        return new, None
    except:
        return None, '--> Download SocksList failed.'


def save_in_redis(proxies):
    Redis = RedisClient(name='raw_proxy')
    raw = {x.decode() for x in Redis.getAll()}
    Redis.delete_all()
    raw.update(proxies)
    for i in raw:
        Redis.put(i)
    print(Redis.get_status(), ' proxies')


if __name__ == '__main__':
    proxies, err = get_socks()
    print(proxies, err)
