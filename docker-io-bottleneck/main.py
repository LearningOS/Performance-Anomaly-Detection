import os
import sys
import random
import hashlib
import subprocess
import multiprocessing as mp
import threading

import setproctitle


def parse_process_stat(f):
    stat = f.readline()
    stat = stat.split(' ')
    utime = int(stat[13])
    stime = int(stat[14])
    cutime = int(stat[15])
    cstime = int(stat[16])
    return utime, stime


def parse_process_status(f):
    lines = f.readlines()
    voluntary_ctxt_switches = int(lines[-2].split(':')[1])
    nonvoluntary_ctxt_switches = int(lines[-1].split(':')[1])
    return voluntary_ctxt_switches, nonvoluntary_ctxt_switches


def parse_stat(f):
    cpu_line = f.readline()
    counts = cpu_line.split()[1:]
    user = int(counts[0])
    nice = int(counts[1])
    system = int(counts[2])
    idle = int(counts[3])
    iowait = int(counts[4])
    return user, nice, system, idle


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

    pre_utime, pre_stime = None, None
    pre_voluntary_ctxt_switches, pre_nonvoluntary_ctxt_switches = None, None

    def loop():
        if not p.is_alive():
            return
        threading.Timer(1, loop).start()
        utime, stime = parse_process_stat(open(stat_file))
        voluntary_ctxt_switches, nonvoluntary_ctxt_switches = \
            parse_process_status(open(status_file))
        nonlocal pre_utime, pre_stime
        nonlocal pre_voluntary_ctxt_switches, pre_nonvoluntary_ctxt_switches
        if pre_utime is not None:
            print(
                utime - pre_utime,
                stime - pre_stime,
                voluntary_ctxt_switches - pre_voluntary_ctxt_switches,
                nonvoluntary_ctxt_switches - pre_nonvoluntary_ctxt_switches
            )
        pre_utime, pre_stime = utime, stime
        pre_voluntary_ctxt_switches, pre_nonvoluntary_ctxt_switches = \
            voluntary_ctxt_switches, nonvoluntary_ctxt_switches

    loop()


if __name__ == '__main__':
    main()
