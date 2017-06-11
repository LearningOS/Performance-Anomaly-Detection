import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


class LocalRelativeDensity(object):
    def __init__(self, n_neighbors=20, contamination=0.1):
        self._nbrs = NearestNeighbors(n_neighbors=n_neighbors)
        self.contamination = contamination
        self._threshold = 0  # type: float
        self._h = None  # type: np.ndarray
        self._X = None  # type: np.ndarray
        self._X_density = None  # type: np.ndarray

    def _kernel(self, X: np.ndarray) -> np.ndarray:
        return np.exp(np.square(X) / 2)

    def _density(self, X: np.ndarray):
        d = X.shape[1]
        distances, indices = self._nbrs.kneighbors(X)  # type: np.ndarray
        # return np.mean(1 / np.power(self._h[indices], d) * self._kernel(
        #     distances / self._h[indices]), axis=-1)
        h = distances.mean(axis=-1)[:, np.newaxis]
        return np.mean(1 / np.power(h, d) * self._kernel(distances / h),
                       axis=-1)

    def fit(self, X: np.ndarray):
        self._nbrs.fit(X)
        self._X = X
        distances, indices = self._nbrs.kneighbors(X)  # type: np.ndarray
        self._h = distances.mean(axis=-1)
        self._X_density = self._density(X)
        return self

    def fit_predict(self, X: np.ndarray):
        return self.fit(X).predict(X)

    def predict(self, X: np.ndarray):
        is_inlier = np.ones(X.shape[0], dtype=int)
        is_inlier[self._decision_function(X) >= 2] = -1
        return is_inlier

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        return self._decision_function(X)

    def _decision_function(self, X: np.ndarray) -> np.ndarray:
        distances, indices = self._nbrs.kneighbors(X)
        density = self._density(X)
        return -np.log(
            np.mean(self._X_density[indices] / density[:, np.newaxis], axis=-1))


class LRDDetector(object):
    def __init__(self):
        self._lrd = LocalRelativeDensity(contamination=0.1)
        self._scaler = StandardScaler()
        # type: sklearn.preprocessing.StandardScaler

    @property
    def scaler(self):
        return self._scaler

    @property
    def lrd(self):
        return self._lrd

    def fit(self, X: np.ndarray):
        X_scaled = self._scaler.fit_transform(X)
        self._lrd.fit(X_scaled)

    def predict(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return self._lrd.predict(X_scaled)

    def score(self, X: np.ndarray):
        X_scaled = self._scaler.transform(X)
        return -self._lrd.decision_function(X_scaled)
