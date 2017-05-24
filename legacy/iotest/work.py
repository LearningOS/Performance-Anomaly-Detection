import os
import argparse
import hashlib

import setproctitle


def main():
    setproctitle.setproctitle('work')
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--file', type=str, required=True, help='the input file')
    args = parser.parse_args()

    m = hashlib.md5()
    with open(args.file) as f:
        for chuck in iter(lambda : f.read(1024), ''):
            m.update(chuck.encode('utf-8'))
    digest = m.hexdigest()
    print(digest)


if __name__ == '__main__':
    main()
