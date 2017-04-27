import os
import sys
import random
import hashlib
import pickle
import subprocess
import multiprocessing as mp
import threading

import numpy as np
import sklearn
import setproctitle

import lof
import utils
import proc_utils


class Detector(object):
    def __init__(self, n_dim, alpha=0.05):
        self._alpha = alpha
        self._mean = np.zeros(n_dim)
        self._square_mean = np.zeros(n_dim)
        self._count = 0

    def detect(self, stats):
        self._count += 1
        stats = np.array(stats)
        print(stats)
        assert stats.shape == self._mean.shape, stats.shape
        std = np.sqrt(self._square_mean - np.square(self._mean))
        print(self._mean)
        print(std)
        condition = (stats > self._mean + 3 * std) | \
            (stats < self._mean - 3 * std)
        anomaly = condition.sum() > 0
        self._mean = self._mean * (1 - self._alpha) + stats * self._alpha
        self._square_mean = self._square_mean * (1 - self._alpha) \
            + np.square(stats) * self._alpha
        return anomaly


class LOFDetector(object):
    def __init__(self, lof_pkl_file, scaler_pkl_file):
        self._clf = pickle.load(open(lof_pkl_file, 'rb'))
        self._scaler = pickle.load(open(scaler_pkl_file, 'rb'))

    def detect(self, stats):
        stats = self._scaler.transform(stats)
        return self._clf._predict(stats)


def cal_file_hash(filename, process_name='hash'):
    setproctitle.setproctitle(process_name)
    m = hashlib.md5()
    with open(filename) as f:
        for chuck in iter(lambda: f.read(1024), ''):
            m.update(chuck.encode('utf-8'))
    digest = m.hexdigest()
    return digest


def random_read_files(dir_path, process_name='reader'):
    setproctitle.setproctitle(process_name)
    for root, dirs, files in os.walk(dir_path):
        random.shuffle(files)
        for filename in files:
            with open(os.path.join(root, filename)) as f:
                lines = f.readlines()


def get_pid_by_name(name):
    pid = subprocess.check_output(['pgrep', '-n', name])
    return int(pid)


def detect_process(pid):
    pass


def main():
    os.system('echo 3 > /proc/sys/vm/drop_caches')

    p = mp.Process(target=cal_file_hash, args=('/data/graduate-project/output.txt',))
    p.start()
    pid = get_pid_by_name('hash')

    base_dir = os.path.join('/proc', str(pid))
    stat_file = os.path.join(base_dir, 'stat')
    status_file = os.path.join(base_dir, 'status')
    fd_dir = os.path.join(base_dir, 'fd')
    system_stat_file = os.path.join('/proc', 'stat')

    detector = LOFDetector('lof.pkl', 'scaler.pkl')

    logfile = open('log.txt', 'w')

    pre_stat = None

    def do_work():
        stat = np.array(proc_utils.parse_stat(open(system_stat_file)))
        nonlocal pre_stat
        if pre_stat is not None:
            stat_diff = stat - pre_stat
            pre_stat = stat
            print(' '.join(map(str, stat_diff)), file=logfile, flush=True)
            print(detector.detect(stat_diff.reshape(1, -1)))
        else:
            pre_stat = stat

    utils.PerpetualTimer(1, do_work, terminal_condition=lambda: not p.is_alive()).start()


if __name__ == '__main__':
    main()
