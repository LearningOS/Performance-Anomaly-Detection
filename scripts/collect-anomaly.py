import os
import sys
import argparse
import subprocess
import shlex

import numpy as np
import pandas as pd

from perf_anomaly.data import *
from perf_anomaly.analyzer import *


def run_command(command, stdinput='', shell=True):
    workload = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                shell=shell,
                                universal_newlines=True,
                                bufsize=0)
    workload.stdin.write(stdinput)
    return workload


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--out', type=str, required=True,
                        help='the output path')
    args = parser.parse_args()

    os.system('echo 3 > /proc/sys/vm/drop_caches')

    workload_command = 'FORCE_TIMES_TO_RUN=10000 phoronix-test-suite batch-run build-linux-kernel'
    workload_input = ''

    fault_commands = [
        'python scripts/fault_inject/io_bottleneck.py --dir /data/graduate-project/data',
        'python scripts/fault_inject/cpu_intensive.py'
    ]

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

    for fault_command in fault_commands:
        fault = run_command(shlex.split(fault_command), shell=False)
        collector.start(terminal_condition=lambda: cnt > 20, first_run=True)
        collector.thread.join()
        fault.terminate()
        cnt = 0

    workload.terminate()

    data = pd.concat(dfs, axis=0)  # type: pd.DataFrame
    data.to_pickle(args.out)


if __name__ == '__main__':
    main()
