import os
import threading
import functools


class PerpetualTimer(object):
    def __init__(self, time_interval, func, terminal_condition=None):
        self._time_interval = time_interval
        self._func = func
        self._terminal_condition = terminal_condition
        self._is_running = False
        self._thread = None

    def _handler(self):
        if self._terminal_condition and self._terminal_condition():
            return
        self._thread = threading.Timer(self._time_interval, self._handler)
        self._thread.start()
        self._func()

    def start(self):
        if not self._is_running:
            self._is_running = True
            self._handler()

    def cancel(self):
        if self._is_running:
            self._thread.cancel()
            self._is_running = False


if __name__ == '__main__':
    cnt = 0

    def work():
        global cnt
        print(cnt)
        cnt += 1

    PerpetualTimer(1, work, lambda: cnt >= 10).start()
