import os
import requests
import setproctitle
import gevent
from gevent import monkey

monkey.patch_all()


def connect(url):
    while True:
        requests.get(url)


def main():
    threads = []
    for i in range(20):
        threads.append(gevent.spawn(connect, 'http://127.0.0.1:8000'))
        gevent.sleep(0.5)
    gevent.joinall(threads)


if __name__ == '__main__':
    setproctitle.setproctitle('client')
    main()
