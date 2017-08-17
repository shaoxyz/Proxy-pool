# -*- coding:utf-8 -*-
# Python3
# File    : app
# Time    : 2017/8/14 13:52
import pickle
import random
import datetime
from getsocks import get_socks
from gethttps import get_https

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify

app = Flask(__name__)


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
def refresh():
    """
    Refresh proxy pool
    """
    get_socks()
    get_https()
    return 'refresh success!'


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=refresh,
    trigger=IntervalTrigger(minutes=10),
    id='refresh_ProxyPool',
    name='Refresh ProxyPool every ten minutes',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    get_socks()
    get_https()
    app.run(host='0.0.0.0',
            port=5000)
    """    
    http_server = WSGIServer(('', 5000), app)
    print('start! 127.0.0.1:5000')
    http_server.serve_forever()
    """
