import os
import random
import gevent
import setproctitle
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()


def application(environ, start_response):
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html')
    ]

    gevent.sleep(seconds=random.expovariate(1), ref=True)

    start_response(status, headers)
    return [b'OK']


if __name__ == '__main__':
    setproctitle.setproctitle('server')
    print('start server at 8000')
    WSGIServer(('', 8000), application).serve_forever()
