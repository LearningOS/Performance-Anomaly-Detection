from typing import List, Tuple

import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler


class GaussianStatistics(object):
    def __init__(self):
        self._scaler = StandardScaler()  # type: sklearn.preprocessing.StandardScaler

    @property
    def scaler(self):
        return self._scaler

    def fit(self, X: np.ndarray):
        pass

    def predict(self, X: np.ndarray):
        pass

    def score(self, X: np.ndarray):
        pass
