#!/usr/bin/env python
import time
import sys



if __name__ == '__main__':
    print(sys.argv[1])
    ts = sys.argv[1]
    print(time.localtime(int(ts)))


