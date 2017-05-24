import os
import subprocess

import numpy as np


class Injector(object):
    def __init__(self, target: str, inject_lamb: int = 4, blank_lamb: int = 10):
        self._counter = 0  # type: int
        self._injected = False  # type: bool
        self._process = None  # type: subprocess.Popen
        self._target = target  # type: str
        self._interval = np.random.poisson(blank_lamb)  # type: int
        self._inject_lamb = inject_lamb
        self._blank_lamb = blank_lamb

    @property
    def injected(self):
        return self._injected

    def start(self):
        self._process = subprocess.Popen(
            self._target.split(),
            env=os.environ
        )

    def stop(self):
        self._process.terminate()

    def trigger(self):
        self._counter += 1
        if self.injected:
            if self._counter == self._interval:
                self.stop()
                self._counter = 0
                self._interval = np.random.poisson(self._blank_lamb)
                self._interval = min(self._interval, 5 * self._blank_lamb)
                self._injected = False
        else:
            if self._counter == self._interval:
                self.start()
                self._counter = 0
                self._interval = np.random.poisson(self._inject_lamb)
                self._interval = min(self._interval, 5 * self._inject_lamb)
                self._injected = True
