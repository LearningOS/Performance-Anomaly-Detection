from typing import List, Tuple

import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope


class IndependentGaussianDetector(object):
    def __init__(self):
        self._scaler = StandardScaler()  # type: sklearn.preprocessing.StandardScaler
        self._elliptic = EllipticEnvelope(contamination=0.1)  # type: sklearn.covariance.EllipticEnvelope

    @property
    def scaler(self):
        return self._scaler

    def fit(self, X: np.ndarray):
        self._scaler.fit_transform(X)

    def predict(self, X: np.ndarray):
        return self.score(X) > 3

    def decision_function(self, X):
        return self.score(X)

    def score(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return np.mean(np.square(X_scaled), axis=1)


class CorrelationGaussianDetector(object):
    def __init__(self):
        self._scaler = StandardScaler()  # type: sklearn.preprocessing.StandardScaler
        self._elliptic = EllipticEnvelope(
            contamination=0.1)  # type: sklearn.covariance.EllipticEnvelope

    @property
    def scaler(self):
        return self._scaler

    def fit(self, X: np.ndarray):
        X_scaled = self._scaler.fit_transform(X)
        self._elliptic.fit(X_scaled)

    def predict(self, X: np.ndarray):
        return self._elliptic.predict(self._scaler.transform(X))

    def score(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return self._elliptic.decision_function(X_scaled)