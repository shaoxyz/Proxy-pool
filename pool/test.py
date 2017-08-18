import time
import requests
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}


def use_socks():
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
    url = 'http://www.xiaohua.com/'

    if use == 'socks':
        proxies = use_socks()
    elif use == 'https':
        proxies = use_https()
    else:
        return 'params wrong'

    while True:
        try:
            r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        except:
            print('err in requests')
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
    for i in range(100):
        use = 'https'
        test(use)
        time.sleep(5)