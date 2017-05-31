from typing import List, Tuple

import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler


class IndependentGaussian(object):
    def __init__(self):
        self._scaler = StandardScaler()  # type: sklearn.preprocessing.StandardScaler

    @property
    def scaler(self):
        return self._scaler

    def fit(self, X: np.ndarray):
        self._scaler.fit_transform(X)

    def predict(self, X: np.ndarray):
        return self.score(X) > 3

    def score(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return np.mean(np.square(X_scaled), axis=1)
