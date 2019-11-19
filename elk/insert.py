#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts='http://192.168.50.51', port=19200)


def do_es_ts(timestr):
    tm = time.strptime(timestr, "%Y-%m-%dT%H:%M:%S+08:00")
    ts = time.mktime(tm)
    other_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # print(other_time)
    return other_time


def read_file():
    count = 0
    actions = []
    with open('/Users/eric/Downloads/alog1', 'r') as f:
        for line in f:
            # print(line.split(" "))
            sp = line.split(" ")
            tmp = dict()
            tmp["ip"] = sp[1]
            tmp["@timestamp"] = do_es_ts(sp[4][1:-1])
            tmp["method"] = sp[5][1:]
            tmp["url"] = sp[6]
            tmp["version"] = sp[7][:-1]
            tmp["status"] = int(sp[9][1:-1])
            tmp["byte"] = int(sp[10])
            tmp["refer"] = sp[12][1:-1]
            tmp["ua"] = sp[13]
            # print(count, json.dumps(tmp, indent=2))
            count = count +1
            # ret = es.index(index="aaa-sichuan-13", body=tmp)
            # print(count, ret['result'])
            # break

            action = {'_op_type': 'index',
                      '_index': 'aaa-sichuan-13',
                      '_type': 'doc',
                      '_source': tmp}
            actions.append(action)
            print(count)


            if (count % 10000 == 0):
                for success, info in helpers.parallel_bulk(es, actions, thread_count=1000):
                    if not success:
                        print('Doc failed', info)
                actions.clear()

    for success, info in helpers.parallel_bulk(es, actions, thread_count=1000):
        if not success:
            print('Doc failed', info)





if __name__ == '__main__':
    read_file()
