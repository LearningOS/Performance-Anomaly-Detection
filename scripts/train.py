import os
import sys
import threading
import subprocess
import pickle
import multiprocessing as mp
from queue import Queue, Empty
import hashlib
import setproctitle
from typing import List, Tuple


from perf_anomaly.data import *
from perf_anomaly.analyzer import *


def get_pid_by_name(name):
    pid = subprocess.check_output(['pgrep', '-n', name])
    return int(pid)


def main():
    os.system('echo 3 > /proc/sys/vm/drop_caches')

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
    collector.start(terminal_condition=lambda: cnt > 200)

    collector.thread.join()

    nr_data = len(dfs)
    data = pd.concat(dfs, axis=0).as_matrix()  # type: np.array
    model = WindowAdaptiveLOF(window_size=nr_data)
    # model = IndependentGaussian()
    model.fit(data)

    pickle.dump(model, open('model.pkl', 'wb'))


if __name__ == '__main__':
    main()
