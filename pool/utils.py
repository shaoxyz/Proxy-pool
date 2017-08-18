# -*- coding:utf-8 -*-
# Python3
# File    : utils
# Time    : 2017/8/16 13:46
# Author  : Shaweb
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

# 实际未使用，用来检测某个代理的可用度
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

# 实际未使用，用来检测某个代理的可用度
def filterProxy_cn(proxy):
    """
    检验国内http(s)代理是否可用
    你可能会想为什么后台跑验证，要用的时候直接拿。
    想法很棒，实际上提前验证并没有什么..用，
    因为，这次验证过了，下次一样失效，所以没必要提前验证另做保存，
    就是质量不高且稳定性差。
    """
    proxies = {'http': 'http://' + proxy,
               'https': 'http://' + proxy}
    try:
        # 响应超过10秒的代理不要
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=10)
        if r.status_code == 200:
            print(proxy, ' is valid')
            return True
    except:
        print(proxy, ' is invalid')
        return False

    
def errorCatch(func):
    """
    一个简单的装饰器，用于捕捉gethttps中可能发生的错误，防止程序运行中断掉，
    发生错误的源自爬虫代理网站服务器。
    """
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return "Http(s) connection error!", e

    return decorate


if __name__ == '__main__':
    proxy = '45.32.193.119:8833'
    filterProxy_cn(proxy)
