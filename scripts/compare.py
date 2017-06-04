import os
import sys
import pickle
import argparse

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

from perf_anomaly.data import *
from perf_anomaly.analyzer import *
from perf_anomaly.injector import *


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--workload', type=str, required=True,
                        help='the workload data path')
    parser.add_argument('--alternative', type=str, required=True,
                        help='the alternative data path')
    args = parser.parse_args()

    workload_df = pd.read_pickle(args.workload)  # type: pd.DataFrame
    alternative_df = pd.read_pickle(args.workload)  # type: pd.DataFrame

    workload_data = workload_df.as_matrix()
    alternative_data = alternative_df.as_matrix()

    model = Forest()
    model.fit(workload_data)

    data = np.concatenate([workload_data, alternative_data], axis=0)
    label = np.concatenate([np.zeros(workload_data.shape[0]),
                            np.ones(workload_data.shape[0])], axis=0)

    score = model.score(data)

    fpr, tpr, thresholds = roc_curve(label, score, pos_label=1)
    roc_auc = roc_auc_score(label, score)

    print(roc_auc)


if __name__ == '__main__':
    main()
