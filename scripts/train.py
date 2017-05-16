import os
import sys
import threading
import subprocess
import multiprocessing as mp
import hashlib
import setproctitle
from typing import List, Tuple


from perf_anomaly.data import *


def cal_file_hash(filename, process_name='hash'):
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
    os.system('echo 3 > /proc/sys/vm/drop_caches')

    p = mp.Process(target=cal_file_hash,
                   args=('/data/graduate-project/output.txt',))
    p.start()
    pid = get_pid_by_name('hash')

    collector = SystemDataCollector()
    collector.register_parser('system', SystemStatParser())
    collector.register_parser('system', SystemLoadAvgParser())
    collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start(terminal_condition=lambda: not p.is_alive())


if __name__ == '__main__':
    main()
