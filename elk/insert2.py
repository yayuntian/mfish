#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import json
import time
from datetime import datetime


def read_file():
    with open('/Users/eric/Downloads/services', 'rb') as f:
        glist = json.load(f)
        # print(json.dumps(glist, indent=2))


        for t in glist:
            out = json.dumps(t, indent=2)
            # print(out)

            try:
                print(t["Spec"]["Name"], t["Spec"]["TaskTemplate"]["Networks"])
            except:
                pass







if __name__ == '__main__':
    read_file()
