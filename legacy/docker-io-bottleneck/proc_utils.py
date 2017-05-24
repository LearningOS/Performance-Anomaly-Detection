import os
import sys


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
    line = f.readline()
    while not line.startswith('cpu'):
        line = f.readline()
    counts = line.split()[1:]
    user = int(counts[0])
    nice = int(counts[1])
    system = int(counts[2])
    idle = int(counts[3])
    iowait = int(counts[4])
    irq = int(counts[5])
    softirq = int(counts[6])

    line = f.readline()
    while not line.startswith('intr'):
        line = f.readline()
    intr = int(line.split()[1])

    line = f.readline()
    while not line.startswith('ctxt'):
        line = f.readline()
    ctxt = int(line.split()[1])

    return user, nice, system, idle, iowait, irq, softirq, intr, ctxt
