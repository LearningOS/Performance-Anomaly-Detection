import os
import sys
import pickle
import threading
import multiprocessing as mp
from queue import Queue, Empty
import hashlib
import setproctitle

import numpy as np
import pandas as pd

from perf_anomaly.data import *
from perf_anomaly.analyzer import *
from perf_anomaly.injector import *


def cal_file_hash(filename, process_name='hash'):
    setproctitle.setproctitle(process_name)
    m = hashlib.md5()
    with open(filename) as f:
        for chuck in iter(lambda: f.read(1024), ''):
            m.update(chuck.encode('utf-8'))
    digest = m.hexdigest()
    return digest


def main():
    os.system('echo 3 > /proc/sys/vm/drop_caches')

    q = Queue()

    scorefile = open('score.txt', 'w')

    tasks = [
        'python scripts/fault_inject/io_bottleneck.py --dir /data/graduate-project/data',
        'python scripts/fault_inject/cpu_intensive.py'
    ]

    injector = Injector(target=tasks[0])

    def collector_callback(df: pd.DataFrame) -> None:
        q.put(df)

    def analyzer_callback(predict, score) -> None:
        print(predict, injector.injected)
        print(score, int(injector.injected), file=scorefile, flush=True)
        # injector.trigger()

    def getter():
        return q.get(block=True, timeout=10)

    analyzer = Analyzer('model.pkl', getter, analyzer_callback)
    analyzer.start()

    collector = SystemDataCollector(5, collector_callback)
    collector.register_parser('system', SystemStatParser())
    # collector.register_parser('system', SystemLoadAvgParser())
    # collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start()

    collector.thread.join()
    analyzer.thread.join()


if __name__ == '__main__':
    main()
