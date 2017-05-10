from perf_anomaly.data import *


if __name__ == '__main__':
    print(SystemStatParser().get_data())
    print(SystemLoadAvgParser().get_data())
    print(SystemMemInfoParser().get_data())
    print(SystemNetworkStatParser().get_data())
    print(SystemDiskStatParser().get_data())
    print(SystemVMStatParser().get_data())
