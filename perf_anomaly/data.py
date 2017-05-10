import os
import abc
import typing
import collections


class BaseParser(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_data(self) -> typing.NamedTuple:
        raise NotImplementedError()


class SystemStatParser(BaseParser):
    # cumulative variable
    SystemStat = collections.namedtuple('SystemStat',
                                        ['user_time', 'nice_time', 'system_time', 'idle_time', 'iowait_time',
                                         'irq', 'softirq', 'intr', 'ctxt'])

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
                                           ['load_1min', 'load_5min', 'load_15min',
                                            'run_threads', 'all_threads'])

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
            run_threads = int(numbers[3].split('/')[0])
            all_threads = int(numbers[3].split('/')[1])

        return self.SystemLoadAvg(
            load_1min=load_1min,
            load_5min=load_5min,
            load_15min=load_15min,
            run_threads=run_threads,
            all_threads=all_threads
        )


class SystemMemInfoParser(BaseParser):
    # instant variable
    SystemMemInfo = collections.namedtuple('SystemMemInfo',
                                           ['mem_total', 'mem_free', 'swap_total', 'swap_free'])

    def __init__(self):
        super(SystemMemInfoParser, self).__init__()
        self._system_meminfo_path = os.path.join('/proc', 'meminfo')

    def get_data(self):
        with open(self._system_meminfo_path) as f:
            lines = f.readlines()
            key_value_map = {k: v for (k, v) in map(lambda l: (l.split()[0][:-1], int(l.split()[1])), lines)}

        return self.SystemMemInfo(
            mem_total=key_value_map['MemTotal'],
            mem_free=key_value_map['MemFree'],
            swap_total=key_value_map['SwapTotal'],
            swap_free=key_value_map['SwapFree']
        )


class SystemNetworkStatParser(BaseParser):
    # cumulative variable
    SystemNetworkStat = collections.namedtuple('SystemNetworkStat',
                                               ['rx_bytes', 'rx_packets', 'rx_errs', 'rx_drops',
                                                'tx_bytes', 'tx_packets', 'tx_errs', 'tx_drops'])

    def __init__(self):
        super(SystemNetworkStatParser, self).__init__()
        self._system_network_stat_path = os.path.join(os.path.join('/proc', 'net'), 'dev')

    def get_data(self) -> SystemNetworkStat:
        with open(self._system_network_stat_path) as f:
            f.readline()
            _, rx, tx = f.readline().split('|')
            rx_attributes = rx.split()
            tx_attributes = tx.split()
            all_iface_lines = f.readlines()
            all_iface_stats = list(map(lambda x: list(map(int, x.split()[1:])), all_iface_lines))
            sum_all_iface = list(map(sum, zip(*all_iface_stats)))
            half = len(sum_all_iface) // 2
            sum_all_iface_rx, sum_all_iface_tx = sum_all_iface[:half], sum_all_iface[half:]

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
                                            ['nr_read', 'nr_read_merge', 'nr_sectors_read', 'ms_read',
                                             'nr_write', 'nr_write_merge', 'nr_sectors_write', 'ms_write',
                                             'nr_io', 'ms_io', 'weighted_ms_io'])

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
                                          ['pgpgin', 'pgpgout', 'pswpin', 'pswpout', 'pgfault'])

    def __init__(self):
        super(SystemVMStatParser, self).__init__()
        self._system_vmstat_path = os.path.join('/proc', 'vmstat')

    def get_data(self) -> SystemVMStat:
        with open(self._system_vmstat_path) as f:
            lines = f.readlines()
            key_value_map = {k: int(v) for k, v in map(lambda x: x.split(), lines)}
        return self.SystemVMStat(**{k: v for k, v in key_value_map.items() if k in self.SystemVMStat._fields})


class SystemDataCollector(object):
    def __init__(self):
        pass

    def register_parser(self, namespace: str, parser: BaseParser):
        pass


if __name__ == '__main__':
    print(SystemStatParser().get_data())
    print(SystemLoadAvgParser().get_data())
    print(SystemMemInfoParser().get_data())
    print(SystemNetworkStatParser().get_data())
    print(SystemDiskStatParser().get_data())
    print(SystemVMStatParser().get_data())
