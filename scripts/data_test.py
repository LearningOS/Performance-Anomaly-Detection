from perf_anomaly.data import *


if __name__ == '__main__':
    # print(SystemStatParser().get_data())
    # print(SystemLoadAvgParser().get_data())
    # print(SystemMemInfoParser().get_data())
    # print(SystemNetworkStatParser().get_data())
    # print(SystemDiskStatParser().get_data())
    # print(SystemVMStatParser().get_data())
    collector = SystemDataCollector()
    collector.register_parser('system', SystemStatParser())
    collector.register_parser('system', SystemLoadAvgParser())
    collector.register_parser('system', SystemMemInfoParser())
    collector.register_parser('system', SystemNetworkStatParser())
    collector.register_parser('system', SystemDiskStatParser())
    collector.register_parser('system', SystemVMStatParser())
    collector.start()
