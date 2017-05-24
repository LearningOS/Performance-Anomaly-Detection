import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--out', type=str, required=True, help='the output path')
    parser.add_argument('--num', type=int, required=True, help='the count of file')
    args = parser.parse_args()

    base_dir = args.out
    for i in range(args.num):
        if i % 1000 == 0:
            print(i)
        with open(os.path.join(base_dir, str(i)), 'w') as f:
            f.write(str(i))


if __name__ == '__main__':
    main()
