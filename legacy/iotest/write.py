import os
import sys
import random
import argparse


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--out', type=str, required=True, help='the output path')
    parser.add_argument('--dir_count', type=int, required=True, help='the count of dir')
    parser.add_argument('--file_count', type=int, required=True, help='the count of file')
    args = parser.parse_args()

    base_dir = args.out
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    order = list(range(args.dir_count * args.file_count))
    random.shuffle(order)
    for idx, index in enumerate(order):
        if idx % 1000 == 0:
            print(idx)
        dirname = str(index // args.file_count)
        filename = str(index % args.file_count)
        dirpath = os.path.join(base_dir, dirname)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        with open(os.path.join(dirpath, filename), 'w') as f:
            f.write(str(random.getrandbits(256)))


if __name__ == '__main__':
    main()
