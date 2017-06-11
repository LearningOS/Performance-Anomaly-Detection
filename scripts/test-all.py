import os
import argparse

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from perf_anomaly.lof import LOFDetector
from perf_anomaly.gaussian import IndependentGaussianDetector
from perf_anomaly.forest import IsolationForestDetector
from perf_anomaly.svm import OneClassSVMDetector


def eval_auc(data_file, normal_file, anomaly_file):
    training_df = pd.read_pickle(data_file)  # type: pd.DataFrame

    normal_df = pd.read_pickle(normal_file)  # type: pd.DataFrame

    anomaly_df = pd.read_pickle(anomaly_file)  # type: pd.DataFrame

    training_data = training_df.as_matrix()
    normal_data = normal_df.as_matrix()
    anomaly_data = anomaly_df.as_matrix()
    # anomaly_data = anomaly_data[40:]

    model = LOFDetector()
    # model = IsolationForestDetector()
    # model = OneClassSVMDetector()
    # model = IndependentGaussianDetector()
    model.fit(training_data)

    data = np.concatenate([normal_data, anomaly_data], axis=0)
    label = np.concatenate([np.zeros(normal_data.shape[0]),
                            np.ones(anomaly_data.shape[0])], axis=0)

    score = model.score(data)

    roc_auc = roc_auc_score(label, score)

    return roc_auc


list_benchmark = [
    'blender',
    'build-linux-kernel',
    'compress-gzip',
    'idle',
    'mcperf.set',
    'n-queens',
    'nginx',
    'pgbench',
    'redis.set',
    'sample-program',
    'scikit-learn',
    'smallpt',
    'sqlite',
    'tensorflow',
    'video-cpu-usage',
    'x264',
    'nginx.workload'
]


def main():
    base_dir = 'log'

    def auc(bench_name):
        data_file = os.path.join(base_dir, bench_name + '.data.pkl')
        normal_file = os.path.join(base_dir, bench_name + '.normal.pkl')
        anomaly_file = os.path.join(base_dir, bench_name + '.anomaly.pkl')
        return eval_auc(data_file, normal_file, anomaly_file)

    result = [(name, auc(name)) for name in list_benchmark]

    for res in result:
        print(res[0] + ': ' + str(res[1]))


if __name__ == '__main__':
    main()
