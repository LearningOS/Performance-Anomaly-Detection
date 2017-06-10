import os
import time
import random
import socket
import argparse

import setproctitle


def main():
    setproctitle.setproctitle('network')
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--ip', type=str, required=True, help='ip address to send traffic')
    args = parser.parse_args()

    random.seed(os.urandom(512))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        time.sleep(0.1)
        for i in range(100):
            sock.sendto(str(random.getrandbits(128)).encode('utf-8'), (args.ip, 22))


if __name__ == '__main__':
    main()
