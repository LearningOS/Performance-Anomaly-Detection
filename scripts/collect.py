import os
import sys
import argparse
import subprocess

import numpy as np
import pandas as pd

from perf_anomaly.data import *
from perf_anomaly.analyzer import *


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
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--out', type=str, required=True,
                        help='the output path')
    args = parser.parse_args()

    os.system('echo 3 > /proc/sys/vm/drop_caches')

    workload_command = 'FORCE_TIMES_TO_RUN=10000 phoronix-test-suite batch-run smallpt'
    workload_input = ''

    workload = run_command(workload_command, workload_input)
    time.sleep(10)

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

    workload.terminate()

    nr_data = len(dfs)
    data = pd.concat(dfs, axis=0)  # type: pd.DataFrame
    data.to_pickle(args.out)


if __name__ == '__main__':
    main()
