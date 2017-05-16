from typing import List, Tuple

import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler

from perf_anomaly import lof


class WindowAdaptiveLOF(object):
    def __init__(self, window_size: int):
        self._X = None  # type: np.ndarray
        self._X_scaled = None  # type: np.ndarray
        self._lof = lof.LocalOutlierFactor()
        self._window_size = window_size
        self._scaler = StandardScaler()  # type: sklearn.preprocessing.StandardScaler

    @property
    def scaler(self):
        return self._scaler

    @property
    def lof(self):
        return self._lof

    def fit(self, X: np.ndarray):
        self._X = X
        self._X_scaled = self._scaler.fit_transform(X)
        self._lof.fit(X)

    def add_new_data_point(self, x):
        if len(self._X) >= self._window_size:
            self._X = np.append(self._X[-self._window_size - 1:], x, axis=0)
        else:
            self._X = np.append(self._X, x, axis=0)
        self._X_scaled = self._scaler.fit_transform(self._X)
        self._lof.fit(self._X_scaled)

    def predict(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return self._lof._predict(X_scaled)
