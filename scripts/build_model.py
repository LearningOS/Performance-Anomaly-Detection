import os
import argparse

import numpy as np
import pandas as pd
import sklearn

from perf_anomaly.data import *
from perf_anomaly.analyzer import *
from perf_anomaly.lof import LOFDetector
from perf_anomaly.forest import IsolationForestDetector


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--data', type=str, required=True,
                        help='the dat path')
    args = parser.parse_args()
    df = pd.read_pickle(args.data)  # type: pd.DataFrame
    model = LOFDetector()
    model.fit(df.as_matrix())
    pickle.dump(model, open('model.pkl', 'wb'))


if __name__ == '__main__':
    main()
