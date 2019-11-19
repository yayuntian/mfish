#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import json
import time
from datetime import datetime


def do_es_ts(timestr):
    tm = time.strptime(timestr, "%Y-%m-%dT%H:%M:%S+08:00")
    ts = time.mktime(tm)
    other_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # print(other_time)
    return other_time


def read_file():
    actions = {}
    with open('/Users/eric/Downloads/ret1', 'r') as f:
        for line in f:
            sp = line.split(" ")
            deviceCode = sp[21][:-1]
            # print(deviceCode)
            if deviceCode.split("=")[1] == "019959993596496":
                print(sp[1:])



if __name__ == '__main__':
    read_file()
