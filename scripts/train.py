import os
import sys
import threading
import subprocess
import pickle
import multiprocessing as mp
from queue import Queue
import hashlib
import setproctitle
from typing import List, Tuple


from perf_anomaly.data import *
from perf_anomaly.adaptive_lof import *


def cal_file_hash(filename, process_name='hash'):
    os.system('echo 3 > /proc/sys/vm/drop_caches')
    setproctitle.setproctitle(process_name)
    m = hashlib.md5()
    with open(filename) as f:
        for chuck in iter(lambda: f.read(1024), ''):
            m.update(chuck.encode('utf-8'))
    digest = m.hexdigest()
    return digest


def get_pid_by_name(name):
    pid = subprocess.check_output(['pgrep', '-n', name])
    return int(pid)


def main():
    p = mp.Process(target=cal_file_hash,
                   args=('/data/graduate-project/output.txt',))
    p.start()
    pid = get_pid_by_name('hash')

    dfs = []  # type: List[pd.DataFrame]

    def callback(df: pd.DataFrame) -> None:
        dfs.append(df)

    collector = SystemDataCollector(1, callback)
    collector.register_parser('system', SystemStatParser())
    collector.register_parser('system', SystemLoadAvgParser())
    collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start(terminal_condition=lambda: not p.is_alive())

    collector.thread.join()

    nr_data = len(dfs)
    data = pd.concat(dfs, axis=0).as_matrix()
    model = WindowAdaptiveLOF(window_size=nr_data)
    model.fit(data)

    pickle.dump(model, 'model.pkl')


if __name__ == '__main__':
    main()
