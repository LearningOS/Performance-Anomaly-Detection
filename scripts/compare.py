import os
import sys
import time
import pickle
import argparse
from queue import Queue, Empty
import hashlib
import setproctitle

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

from perf_anomaly.data import *
from perf_anomaly.analyzer import *
from perf_anomaly.injector import *


def train(counts=200):
    dfs = []  # type: List[pd.DataFrame]

    cnt = 0

    def callback(df: pd.DataFrame) -> None:
        nonlocal cnt
        cnt += 1
        dfs.append(df)
        print(df)

    collector = SystemDataCollector(5, callback)
    collector.register_parser('system', SystemStatParser())
    # collector.register_parser('system', SystemLoadAvgParser())
    # collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start(terminal_condition=lambda: cnt > counts)

    collector.thread.join()

    nr_data = len(dfs)
    data = pd.concat(dfs, axis=0).as_matrix()  # type: np.array
    # model = WindowAdaptiveLOF(window_size=nr_data)
    # model = IndependentGaussian()
    model = Forest()
    model.fit(data)

    pickle.dump(model, open('model.pkl', 'wb'))
    return model


def run_command(command, stdinput=''):
    workload = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                shell=True,
                                universal_newlines=True,
                                bufsize=0)
    workload.stdin.write(stdinput)
    return workload

def main():
    os.system('echo 3 > /proc/sys/vm/drop_caches')

    workload_command = 'FORCE_TIMES_TO_RUN=10000 phoronix-test-suite batch-run compress-gzip'
    workload_input = ''
    alternative_command = 'FORCE_TIMES_TO_RUN=10000 phoronix-test-suite batch-run sample-program'
    alternative_input = ''

    workload = run_command(workload_command, workload_input)
    time.sleep(10)

    model = train()

    workload.terminate()

    q = Queue()

    scores = []
    labels = []
    cnt = 0
    workload = None  # type: subprocess.Popen

    def collector_callback(df: pd.DataFrame) -> None:
        q.put(df)

    def analyzer_callback(predict, score) -> None:
        nonlocal cnt
        nonlocal workload
        scores.append(score)
        print(score)
        if cnt == 0:
            workload = run_command(workload_command, workload_input)
        elif cnt == 100:
            workload.terminate()
            workload = run_command(alternative_command, alternative_input)
        elif cnt == 200:
            workload.terminate()

        if cnt < 100:
            labels.append(0)
        else:
            labels.append(1)
        cnt += 1

    def getter():
        return q.get(block=True, timeout=10)

    analyzer = Analyzer(model, getter, analyzer_callback)
    analyzer.start(terminal_condition=lambda: cnt > 200)

    collector = SystemDataCollector(5, collector_callback)
    collector.register_parser('system', SystemStatParser())
    # collector.register_parser('system', SystemLoadAvgParser())
    # collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start(terminal_condition=lambda: cnt > 200)

    collector.thread.join()
    analyzer.thread.join()

    scores = np.array(scores)
    labels = np.array(labels)

    fpr, tpr, thresholds = roc_curve(labels, scores, pos_label=1)
    roc_auc = roc_auc_score(labels, scores)
    print(roc_auc)


if __name__ == '__main__':
    main()
