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
from perf_anomaly.gaussian import CorrelationGaussianDetector
from perf_anomaly.forest import IsolationForestDetector
from perf_anomaly.svm import OneClassSVMDetector


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--data', type=str, required=True, nargs='+',
                        help='the training data path')
    parser.add_argument('--normal', type=str, required=True, nargs='+',
                        help='the normal data path')
    parser.add_argument('--anomaly', type=str, required=True, nargs='+',
                        help='the anomaly data path')
    args = parser.parse_args()

    training_df = pd.concat([pd.read_pickle(df_file) for df_file in args.data],
                            axis=0)  # type: pd.DataFrame

    normal_df = pd.concat([pd.read_pickle(df_file) for df_file in args.normal],
                          axis=0)  # type: pd.DataFrame

    anomaly_df = pd.concat([pd.read_pickle(df_file) for df_file in args.anomaly],
                           axis=0)  # type: pd.DataFrame

    training_data = training_df.as_matrix()
    normal_data = normal_df.as_matrix()
    anomaly_data = anomaly_df.as_matrix()

    # model = IndependentGaussianDetector()
    # model = OneClassSVMDetector()
    # model = IsolationForestDetector()
    model = LOFDetector()
    model.fit(training_data)

    data = np.concatenate([normal_data, anomaly_data], axis=0)
    label = np.concatenate([np.zeros(normal_data.shape[0]),
                            np.ones(anomaly_data.shape[0])], axis=0)

    score = model.score(data)

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
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':
    main()
