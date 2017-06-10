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

    # workload_command = 'FORCE_TIMES_TO_RUN=10000 phoronix-test-suite batch-run scikit-learn'
    # workload_input = ''
    #
    # workload = run_command(workload_command, workload_input)
    # time.sleep(10)

    q = Queue()

    scorefile = open('score.txt', 'w')

    tasks = [
        'python scripts/fault_inject/io_bottleneck.py --dir /data/graduate-project/data',
        'python scripts/fault_inject/cpu_intensive.py',
        'python scripts/fault_inject/network_traffic.py --ip 172.17.0.2'
    ]

    injector = Injector(target=tasks[1])

    def collector_callback(df: pd.DataFrame) -> None:
        q.put(df)

    def analyzer_callback(predict, score) -> None:
        print(predict, injector.injected)
        print(score, int(injector.injected), file=scorefile, flush=True)
        injector.trigger()

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

    # workload.terminate()


if __name__ == '__main__':
    main()
