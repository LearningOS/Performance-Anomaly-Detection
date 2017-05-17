import os
import random


def main():
    obj_list = []
    while True:
        obj_list.append(random.getrandbits(128))


if __name__ == '__main__':
    main()
