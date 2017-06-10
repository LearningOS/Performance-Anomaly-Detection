import os
import sys
import signal
import argparse
import subprocess

import numpy as np
import pandas as pd

from perf_anomaly.data import *
from perf_anomaly.analyzer import *


tasks = {
    'pgbench': (
        'FORCE_TIMES_TO_RUN=100000 phoronix-test-suite batch-run pgbench',
        '3\n2\n1\n'
    ),
    'build-linux-kernel': (
        'FORCE_TIMES_TO_RUN=100000 phoronix-test-suite batch-run build-linux-kernel',
        ''
    )
}


fault_commands = [
    'python scripts/fault_inject/cpu_intensive.py',
    'python scripts/fault_inject/io_bottleneck.py --dir /data/graduate-project/data',
    'python scripts/fault_inject/network_traffic.py --ip 172.17.0.2'
]


def run_command(command, stdinput=''):
    workload = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                shell=True,
                                start_new_session=True,
                                universal_newlines=True,
                                bufsize=0)
    workload.stdin.write(stdinput)
    return workload


def collect_task(taskname, nr_time, outfile, inject=False):
    workload_command, workload_input = tasks[taskname]

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

    workload = run_command(workload_command, workload_input)
    time.sleep(10)

    if inject:
        for fault_command in fault_commands:
            fault = run_command(fault_command)
            collector.start(terminal_condition=lambda: cnt >= nr_time, first_run=True)
            collector.thread.join()
            os.killpg(os.getpgid(fault.pid), signal.SIGTERM)
            cnt = 0
    else:
        collector.start(terminal_condition=lambda: cnt >= nr_time, first_run=True)
        collector.thread.join()

    os.killpg(os.getpgid(workload.pid), signal.SIGTERM)
    data = pd.concat(dfs, axis=0)  # type: pd.DataFrame
    data.to_pickle(outfile)


def main():
    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument('--out', type=str, required=True,
    #                     help='the output path')
    # args = parser.parse_args()

    os.system('echo 3 > /proc/sys/vm/drop_caches')

    taskname = 'build-linux-kernel'

    collect_task(taskname, 1000, os.path.join('log', taskname + '.data.pkl'))
    time.sleep(60)
    collect_task(taskname, 300, os.path.join('log', taskname + '.normal.pkl'))
    time.sleep(60)
    collect_task(taskname, 100, os.path.join('log', taskname + '.anomaly.pkl', inject=True))

if __name__ == '__main__':
    main()
