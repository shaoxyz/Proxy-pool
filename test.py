"""
关于如何使用该代理池的小爬虫示例。
前提是开启代理池服务，python app.py
"""

import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from utils import verifyProxyFormat

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}


def use_sock():
    proxy = requests.get('http://localhost:5000/getsocks/').text
    # proxy = '127.0.0.1:1080'
    proxies = {'http': 'socks5://' + proxy,
               'https': 'socks5://' + proxy}
    return proxies


def use_https():
    proxy = requests.get('http://localhost:5000/gethttps/').text
    # proxy = '127.0.0.1:1080'
    proxies = {'http': 'http://' + proxy,
               'https': 'http://' + proxy}
    return proxies


def test(use='socks'):
    """
    毕竟是免费的代理池，所以质量低且稳定性较差，解决方案：循环直到抽到可用代理，
    个人觉得只适合对代理有一定需求且不追求速度的小爬虫项目，
    大项目..您还是花点银子吧。^_^
    """
    while True:
        if use == 'socks':
            proxies = use_sock()
        elif use == 'https':
            proxies = use_https()
        else:
            return 'params wrong'
        url = 'http://www.xiaohua.com/'  # 随便选的一个笑话网站，如果请求成功就返回第一条笑话。
        try:
            r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        except:
            print('requests err')
            continue
        if r.status_code == 200:
            html = etree.HTML(r.text)
            xiaohua = html.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/p/a/text()')[0]
            break
        else:
            print(r.status_code)
            continue
    print(xiaohua)


if __name__ == '__main__':
    """
    做好满篇requests err的准备吧, 
    网上免费公布的代理就是这样=。=
    """
    for i in range(100):
        use = 'https'
        test(use)
        time.sleep(5)
