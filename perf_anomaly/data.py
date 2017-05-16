import os
import abc
import time
import threading
import collections
from typing import Tuple, List, NamedTuple, Callable

import numpy as np
import pandas as pd

from perf_anomaly import utils


class BaseParser(metaclass=abc.ABCMeta):
    cumulative = NamedTuple('Base', [])  # type: NamedTuple

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_data(self) -> NamedTuple:
        raise NotImplementedError()


class SystemStatParser(BaseParser):
    # cumulative variable
    SystemStat = collections.namedtuple('SystemStat',
                                        ['user_time', 'nice_time',
                                         'system_time', 'idle_time',
                                         'iowait_time',
                                         'irq', 'softirq', 'intr', 'ctxt'])
    cumulative = SystemStat(
        user_time=True,
        nice_time=True,
        system_time=True,
        idle_time=True,
        iowait_time=True,
        irq=True,
        softirq=True,
        intr=True,
        ctxt=True
    )

    def __init__(self):
        super(SystemStatParser, self).__init__()
        self._system_stat_path = os.path.join('/proc', 'stat')

    def get_data(self) -> SystemStat:
        with open(self._system_stat_path) as f:
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

        return self.SystemStat(
            user_time=user,
            nice_time=nice,
            system_time=system,
            idle_time=idle,
            iowait_time=iowait,
            irq=irq,
            softirq=softirq,
            intr=intr,
            ctxt=ctxt
        )


class SystemLoadAvgParser(BaseParser):
    # instant variable
    SystemLoadAvg = collections.namedtuple('SystemLoadAvg',
                                           ['load_1min', 'load_5min',
                                            'load_15min'])
    cumulative = SystemLoadAvg(
        load_1min=False,
        load_5min=False,
        load_15min=False,
    )

    def __init__(self):
        super(SystemLoadAvgParser, self).__init__()
        self._system_loadavg_path = os.path.join('/proc', 'loadavg')

    def get_data(self) -> SystemLoadAvg:
        with open(self._system_loadavg_path) as f:
            line = f.readline()
            numbers = line.split()
            load_1min = float(numbers[0])
            load_5min = float(numbers[1])
            load_15min = float(numbers[2])

        return self.SystemLoadAvg(
            load_1min=load_1min,
            load_5min=load_5min,
            load_15min=load_15min,
        )


class SystemMemInfoParser(BaseParser):
    # instant variable
    SystemMemInfo = collections.namedtuple('SystemMemInfo',
                                           ['mem_total', 'mem_free',
                                            'swap_total', 'swap_free'])
    cumulative = SystemMemInfo(
        mem_total=False,
        mem_free=False,
        swap_total=False,
        swap_free=False
    )

    def __init__(self):
        super(SystemMemInfoParser, self).__init__()
        self._system_meminfo_path = os.path.join('/proc', 'meminfo')

    def get_data(self):
        with open(self._system_meminfo_path) as f:
            lines = f.readlines()
            key_value_map = {k: v for (k, v) in map(
                lambda l: (l.split()[0][:-1], int(l.split()[1])), lines)}

        return self.SystemMemInfo(
            mem_total=key_value_map['MemTotal'],
            mem_free=key_value_map['MemFree'],
            swap_total=key_value_map['SwapTotal'],
            swap_free=key_value_map['SwapFree']
        )


class SystemNetworkStatParser(BaseParser):
    # cumulative variable
    SystemNetworkStat = collections.namedtuple('SystemNetworkStat',
                                               ['rx_bytes', 'rx_packets',
                                                'rx_errs', 'rx_drops',
                                                'tx_bytes', 'tx_packets',
                                                'tx_errs', 'tx_drops'])
    cumulative = SystemNetworkStat(
        rx_bytes=True,
        rx_packets=True,
        rx_errs=True,
        rx_drops=True,
        tx_bytes=True,
        tx_packets=True,
        tx_errs=True,
        tx_drops=True
    )

    def __init__(self):
        super(SystemNetworkStatParser, self).__init__()
        self._system_network_stat_path = os.path.join(
            os.path.join('/proc', 'net'), 'dev')

    def get_data(self) -> SystemNetworkStat:
        with open(self._system_network_stat_path) as f:
            f.readline()
            _, rx, tx = f.readline().split('|')
            rx_attributes = rx.split()
            tx_attributes = tx.split()
            all_iface_lines = f.readlines()
            all_iface_stats = list(
                map(lambda x: list(map(int, x.split()[1:])), all_iface_lines))
            sum_all_iface = list(map(sum, zip(*all_iface_stats)))
            half = len(sum_all_iface) // 2
            sum_all_iface_rx, sum_all_iface_tx = sum_all_iface[
                                                 :half], sum_all_iface[half:]

        return self.SystemNetworkStat(
            rx_bytes=sum_all_iface_rx[rx_attributes.index('bytes')],
            rx_packets=sum_all_iface_rx[rx_attributes.index('packets')],
            rx_errs=sum_all_iface_rx[rx_attributes.index('errs')],
            rx_drops=sum_all_iface_rx[rx_attributes.index('drop')],
            tx_bytes=sum_all_iface_tx[tx_attributes.index('bytes')],
            tx_packets=sum_all_iface_tx[tx_attributes.index('packets')],
            tx_errs=sum_all_iface_tx[tx_attributes.index('errs')],
            tx_drops=sum_all_iface_tx[tx_attributes.index('drop')],
        )


class SystemDiskStatParser(BaseParser):
    # cumulative variable
    SystemDiskStat = collections.namedtuple('SystemDiskStat',
                                            ['nr_read', 'nr_read_merge',
                                             'nr_sectors_read', 'ms_read',
                                             'nr_write', 'nr_write_merge',
                                             'nr_sectors_write', 'ms_write',
                                             'nr_io', 'ms_io',
                                             'weighted_ms_io'])
    cumulative = SystemDiskStat(*([True] * len(SystemDiskStat._fields)))

    def __init__(self):
        super(SystemDiskStatParser, self).__init__()
        self._system_disk_stat_path = os.path.join('/proc', 'diskstats')

    def get_data(self):
        with open(self._system_disk_stat_path) as f:
            stats = [0] * len(self.SystemDiskStat._fields)
            for l in f.readlines():
                fields = l.split()
                if fields[2][-1].isdigit():
                    continue
                else:
                    stats = [x + y for x, y in zip(stats, map(int, fields[3:]))]
        return self.SystemDiskStat(*stats)


class SystemVMStatParser(BaseParser):
    # cumulative variable
    SystemVMStat = collections.namedtuple('SystemVMStat',
                                          ['pgpgin', 'pgpgout', 'pswpin',
                                           'pswpout', 'pgfault'])
    cumulative = SystemVMStat(*([True] * len(SystemVMStat._fields)))

    def __init__(self):
        super(SystemVMStatParser, self).__init__()
        self._system_vmstat_path = os.path.join('/proc', 'vmstat')

    def get_data(self) -> SystemVMStat:
        with open(self._system_vmstat_path) as f:
            lines = f.readlines()
            key_value_map = {k: int(v) for k, v in
                             map(lambda x: x.split(), lines)}
        return self.SystemVMStat(**{k: v for k, v in key_value_map.items() if
                                    k in self.SystemVMStat._fields})


# call each registered parser in a certain time period
class SystemDataCollector(object):
    def __init__(self, time_interval: int,
                 callback: Callable[[pd.DataFrame], None]):
        self._parsers = []  # type: List[Tuple[str, BaseParser]]
        self._pre_pd = pd.DataFrame()  # type: pd.DataFrame
        self._time_interval = time_interval  # type: int
        self._pd_cumulative = pd.DataFrame()  # type: pd.DataFrame
        self._callback = callback
        self._thread = None  # type: threading.Thread

    def register_parser(self, namespace: str, parser: BaseParser) -> None:
        self._parsers.append((namespace, parser))

    def _worker_func(self):
        pds = []  # type: List[pd.DataFrame]
        for namespace, parser in self._parsers:
            data = parser.get_data()
            data_pd = pd.DataFrame([data], columns=list(
                map(lambda s: '/'.join([namespace, s]), data._fields)))
            pds.append(data_pd)
        pd_all = pd.concat(pds, axis=1)  # type: pd.DataFrame
        # difference should divided by time interval
        pd_res = (pd_all * self._pd_cumulative
                  - self._pre_pd * self._pd_cumulative) / self._time_interval \
                 + pd_all * (1 - self._pd_cumulative)
        # pd_res = pd_all - self._pre_pd * self._pd_cumulative
        self._pre_pd = pd_all
        self._callback(pd_res)

    @property
    def thread(self) -> threading.Thread:
        return self._thread

    def start(self, terminal_condition=None) -> None:
        pds = []  # type: List[pd.DataFrame]
        for namespace, parser in self._parsers:
            cumulative = parser.cumulative
            cumulative_pd = pd.DataFrame([cumulative],
                                         columns=list(map(
                                             lambda s: '/'.join([namespace, s]),
                                             cumulative._fields)))
            pds.append(cumulative_pd)
        self._pd_cumulative = pd.concat(pds, axis=1).astype(
            'int')  # type: pd.DataFrame
        self._pre_pd = pd.DataFrame(0, index=[0],
                                    columns=self._pd_cumulative.columns.values)
        self._worker_func()

        def target():
            timer = utils.PerpetualTimer(self._time_interval, self._worker_func,
                                         terminal_condition=terminal_condition)
            timer.start()
            while timer.is_running:
                time.sleep(self._time_interval)

        self._thread = threading.Thread(target=target)
        self._thread.start()
