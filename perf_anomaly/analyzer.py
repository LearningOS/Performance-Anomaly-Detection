import os
import sys
import pickle
import threading
from queue import Queue, Empty
from typing import Callable

import numpy as np
import pandas as pd


class Analyzer(object):
    def __init__(self, model, getter,
                 callback: Callable[[int, float], None] = None):
        self._thread = None  # threading.Thread
        if isinstance(model, str):
            self._model = pickle.load(open(model, 'rb'))
        else:
            self._model = model
        self._getter = getter
        self._callback = callback
        self._terminal_condition = None

    @property
    def thread(self) -> threading.Thread:
        return self._thread

    def _target(self):
        try:
            while self._terminal_condition is None or not self._terminal_condition():
                df = self._getter()
                data = df.as_matrix()
                predict = self._model.predict(data)[0]
                score = self._model.score(data)[0]
                if self._callback is not None:
                    self._callback(predict, score)
        except Empty as e:
            return

    def start(self, terminal_condition=None) -> None:
        self._terminal_condition = terminal_condition
        self._thread = threading.Thread(target=self._target, daemon=True)
        self._thread.start()
