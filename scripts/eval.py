import os
import sys
import pickle
import argparse

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

from perf_anomaly.data import *
from perf_anomaly.analyzer import *
from perf_anomaly.injector import *
from perf_anomaly.lof import WindowAdaptiveLOF
from perf_anomaly.lof import LOFDetector
from perf_anomaly.gaussian import IndependentGaussianDetector
from perf_anomaly.forest import IsolationForestDetector
from perf_anomaly.svm import OneClassSVMDetector


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--workload', type=str, required=True,
                        help='the workload data path')
    parser.add_argument('--alternative', type=str, required=True,
                        help='the alternative data path')
    args = parser.parse_args()

    workload_df = pd.read_pickle(args.workload)  # type: pd.DataFrame
    alternative_df = pd.read_pickle(args.alternative)  # type: pd.DataFrame

    workload_data = workload_df.as_matrix()
    alternative_data = alternative_df.as_matrix()

    model = LOFDetector()
    # model = IsolationForestDetector()
    # model = OneClassSVMDetector()
    # model = IndependentGaussianDetector()
    model.fit(workload_data)

    data = np.concatenate([workload_data, alternative_data], axis=0)
    label = np.concatenate([np.zeros(workload_data.shape[0]),
                            np.ones(alternative_data.shape[0])], axis=0)

    score = model.score(data)
    print(score)

    fpr, tpr, thresholds = roc_curve(label, score, pos_label=1)
    roc_auc = roc_auc_score(label, score)

    print(roc_auc)

    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':
    main()
