import gevent
from gevent.monkey import patch_all
patch_all()

import os
import time
import random

import requests


targets = [
    'http://fit.hqythu.me',
    'http://fit.hqythu.me/styles/main.css',
    'http://fit.hqythu.me/styles/vendor.css',
    'http://fit.hqythu.me/scripts/main.js',
    'http://fit.hqythu.me/scripts/vendor.js',
    'http://fit.hqythu.me/fonts/fontawesome-webfont.woff2',
    'http://fit.hqythu.me/images/avatar.jpg'
]


def workload(t):
    for i in range(int(10 / t)):
        time.sleep(random.expovariate(1 / t))
        resp = [requests.get(target) for target in targets]


def process_func(t):
    threads = []
    for i in range(100):
        threads.append(gevent.spawn(workload, t))
    gevent.joinall(threads)


def main():
    while True:
        t = random.random() * 10
        # with Pool(4) as pool:
        #     for i in range(4):
        #         pool.apply_async(process_func, args=(t,))
        #     # for i in range(100):
        #     #     threads.append(gevent.spawn(workload, t))
        #     # gevent.joinall(threads)
        process_func(t)


if __name__ == '__main__':
    main()
