import os
import time
import random
import argparse

import setproctitle


def main():
    setproctitle.setproctitle('reader')
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dir', type=str, required=True, help='the input dir')
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.dir):
        random.shuffle(files)
        for filename in files:
            # time.sleep(0.1)
            with open(os.path.join(root, filename)) as f:
                lines = f.readlines()


if __name__  == '__main__':
    main()
