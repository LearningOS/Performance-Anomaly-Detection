from typing import List, Tuple

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class Forest(object):
    def __init__(self):
        self._scaler = StandardScaler()
        # type: sklearn.preprocessing.StandardScaler
        self._forest = IsolationForest(contamination=0.02)
        # type: sklearn.preprocessing.IsolationForest

    @property
    def scaler(self):
        return self._scaler

    def fit(self, X: np.ndarray):
        X_scaled = self._scaler.fit_transform(X)
        self._forest.fit(X_scaled)

    def predict(self, X: np.array):
        X_scaled = self._scaler.transform(X)
        return self._forest.predict(X_scaled)

    def score(self, X: np.array):
        X_scaled = self._scaler.transform(X)
        return self._forest.decision_function(X_scaled)
