import os
import random
import time
import setproctitle


def main():
    setproctitle.setproctitle('cpu')
    random.seed(os.urandom(512))
    while True:
        arr = [random.randint(0, 100000000) for i in range(100000000)]
        arr.sort()


if __name__ == '__main__':
    main()
