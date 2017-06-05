import os
import sys
import random
import requests
import argparse
import setproctitle
import gevent
from gevent import monkey

monkey.patch_all()


def connect(url):
    while True:
        gevent.sleep(random.expovariate(2))
        requests.get(url)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hosts', type=str, default='http://127.0.0.1:8000')
    args = parser.parse_args()
    threads = []
    for i in range(100):
        threads.append(gevent.spawn(connect, args.hosts))
    gevent.joinall(threads)


if __name__ == '__main__':
    setproctitle.setproctitle('client')
    main()
