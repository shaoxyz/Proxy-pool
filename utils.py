# -*- coding:utf-8 -*-
import requests


def crack(captcha):
    """
    用以破解验证码
    """
    match_ = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
              'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10}
    a, operator, b = captcha.split(' ')[:3]
    a = match_[a] if a in match_ else int(a)
    b = match_[b] if b in match_ else int(b)
    if operator in ['multiplied', 'X']:
        return a * b
    elif operator in ['plus', '+']:
        return a + b
    elif operator in ['minus', '-']:
        return a - b
    else:
        raise IOError


def filterProxy_ab(proxy):
    """
    检验国外socks代理是否可用
    """
    proxies = {'http': 'socks5://' + proxy,
               'https': 'socks5://' + proxy}
    try:
        # 超过10秒的代理不要
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=10)
        if r.status_code == 200:
            return True
    except:
        return False


def filterProxy_cn(proxy):
    """
    检验国内http(s)代理是否可用
    """
    proxies = {'http': 'http://' + proxy,
               'https': 'http://' + proxy}
    try:
        # 超过10秒的代理不要
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=10)
        if r.status_code == 200:
            print(proxy, ' is valid')
            return True
    except:
        try:
            r = requests.get('https://www.baidu.com', proxies=proxies, timeout=10)
            if r.status_code == 200:
                print(proxy, ' is valid')
                return True
        except:
            print(proxy, ' is invalid')
            return False


if __name__ == '__main__':
    proxy = '45.32.193.119:8833'
    filterProxy_cn(proxy)


