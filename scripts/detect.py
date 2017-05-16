import os
import sys
import pickle
import threading
from queue import Queue
import hashlib
import setproctitle

import numpy as np
import pandas as pd

from perf_anomaly.data import *


def cal_file_hash(filename, process_name='hash'):
    setproctitle.setproctitle(process_name)
    m = hashlib.md5()
    with open(filename) as f:
        for chuck in iter(lambda: f.read(1024), ''):
            m.update(chuck.encode('utf-8'))
    digest = m.hexdigest()
    return digest


class Analyzer(object):
    def __init__(self, cls_pkl, scaler_pkl):
        self._thread = None

    def start(self):
        pass


def main():
    q = Queue()

    def callback(df: pd.DataFrame) -> None:
        q.put(df)

    collector = SystemDataCollector(1, callback)
    collector.register_parser('system', SystemStatParser())
    collector.register_parser('system', SystemLoadAvgParser())
    collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start()


if __name__ == '__main__':
    main()
