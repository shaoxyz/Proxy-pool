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
monkey.patch_all()


@app.route('/')
def index():
    info = {
        'Title': u'Proxy-pool',
        'Method': [u'/socks  --> get a sock proxy',
                   u'/https  --> get a http(s) proxy',
                   u'/refresh  --> refresh proxies'],
        'Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(info)


@app.route('/socks/')
def socks():
    """
    Return a proxy and refresh when socks < 20
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


@app.route('/https/')
def https():
    """
    Return a proxy and refresh when socks < 20
    """
    https = pickle.load(open("https.pickle", "rb"))
    if len(https) < 20:
        result, err = get_https()
        if err:
            return err
    http = random.choice(list(https))
    https.remove(http)
    with open('https.pickle', 'wb') as f:
        pickle.dump(https, f, protocol=pickle.HIGHEST_PROTOCOL)
    return http


@app.route('/refresh/')
def schedule():
    """
    Start a schedule to refresh proxy pool, don't need to wait for response
    """
    import time
    get_socks()
    get_https()
    print('refresh task has been on..')
    time.sleep(600)
    return schedule()


if __name__ == '__main__':
    get_socks()
    get_https()
    http_server = WSGIServer(('', 5000), app)
    print('start! 127.0.0.1:5000')
    http_server.serve_forever()
