# -*- coding:utf-8 -*-
# Python3
# File    : app
# Time    : 2017/8/14 13:52
import pickle
import random
import datetime
from getsocks import get_socks
from gethttps import get_https
from flask import Flask, jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
monkey.patch_all()  # 猴子补丁


@app.route('/')
def index():
    info = {
        'Title': u'Proxy-pool',
        'Method': [u'/getsocks  --> get a sock proxy',
                   u'/gethttps  --> get a http(s) proxy',
                   u'/refresh  --> refresh proxies'],
        'Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(info)


@app.route('/getsocks/')
def getsocks():
    """
    return a proxy and refresh when socks < 20
    """
    socks = pickle.load(open("socks.pickle", "rb"))
    if len(socks) < 20:
        result, err = get_socks()
        if err:
            return err
    sock = random.choice(list(socks))
    socks.remove(sock)
    with open('socks.pickle', 'wb') as f:
        pickle.dump(socks, f, protocol=pickle.HIGHEST_PROTOCOL)
    return sock


@app.route('/gethttps/')
def gethttps():
    """
    return a proxy and refresh when socks < 20
    """
    https = pickle.load(open("https.pickle", "rb"))
    if len(https) < 20:
        result, err = get_https()
        if err:
            return err
    sock = random.choice(list(https))
    https.remove(sock)
    with open('https.pickle', 'wb') as f:
        pickle.dump(https, f, protocol=pickle.HIGHEST_PROTOCOL)
    return sock


@app.route('/startrefreshtask/')
def schedule():
    """
    start a schedule to refresh proxy pool
    非阻塞方法，请求一次就开启了定时刷新代理的任务，
    不用等待页面返回，因为没有返回..
    你可以在启动app的命令行，看到刷新成功的输出。
    """
    import time
    while True:
        get_socks()
        get_https()
        print('refresh task has been on..proxies will refresh 10m later!')
        time.sleep(600)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    print('start! 127.0.0.1:5000')
    http_server.serve_forever()
