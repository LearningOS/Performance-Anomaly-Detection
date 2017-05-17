import os
import sys
import pickle
import threading
from queue import Queue, Empty

import numpy as np
import pandas as pd

from perf_anomaly.adaptive_lof import *


class Analyzer(object):
    def __init__(self, model_pkl, getter):
        self._thread = None  # threading.Thread
        self._model = pickle.load(
            open(model_pkl, 'rb'))  # type: WindowAdaptiveLOF
        self._getter = getter

    @property
    def thread(self) -> threading.Thread:
        return self._thread

    def _target(self):
        try:
            while True:
                df = self._getter()
                data = df.as_matrix()
                predict = self._model.predict(data)
                print(predict)
        except Empty as e:
            return

    def start(self):
        self._thread = threading.Thread(target=self._target, daemon=True)
        self._thread.start()
