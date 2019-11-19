#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import json
import time
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts='http://localhost', port=9200)
# es = Elasticsearch(hosts='http://192.168.50.51', port=19200)
# es = Elasticsearch(hosts='https://kunlun.ssl.ysten.com/elasticsearch/', http_auth=('elasticsearch', 'elasticsearch.123'))


def do_es_ts(timestr):
    tm = time.strptime(timestr, "%Y-%m-%dT%H:%M:%S+08:00")
    ts = time.mktime(tm)
    other_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # print(other_time)
    return other_time



def dir():
    for root,dirs,files in os.walk('/Users/eric/Downloads/TMS/西区/'):
        for file in files:
            # print(root)
            if file == ".DS_Store":
                continue

            path = os.path.join(root, file)
            print(path)
            read_file(path)



def read_file(file):
    count = 0
    actions = []
    # file = '/Users/eric/Downloads/ucs-bug/tms10.25.172.62.log'
    with open(file, 'r') as f:
        for line in f:
            # print(line.split(" "))
            ss = 1
            sp = line.split(" ")
            tmp = dict()
            tmp["ip"] = sp[0 + ss]
            tmp["@timestamp"] = do_es_ts(sp[3+ ss][1:-1])
            tmp["method"] = sp[4+ ss][1:]
            tmp["url"] = sp[5+ ss]
            tmp["version"] = sp[6+ ss][:-1]
            tmp["status"] = int(sp[8+ ss][1:-1])
            tmp["byte"] = int(sp[9+ ss])
            # tmp["refer"] = sp[13][1:-1]
            tmp["ua"] = sp[13+ ss][1:]
            cuator = 0
            if sp[13+ ss][1:-1] == "*/*":
                cuator = -2
            if sp[14+ ss] == "":
                cuator = 1
            tmp["duration"] = float(sp[17 + cuator + ss][1:-1])
            tmp["host"] = sp[19 + cuator + ss][1:-1]
            tmp["port"] = int(sp[20 + cuator + ss][1:-1])
            # print(count, json.dumps(tmp, indent=2))
            # print(count, tmp["duration"])
            count = count +1

            action = {'_op_type': 'index',
                      '_index': 'tms-all',
                      '_type': 'doc',
                      '_source': tmp}
            actions.append(action)
            print(count)


            if (count % 1000 == 0):
                for success, info in helpers.parallel_bulk(es, actions, thread_count=1000):
                    if not success:
                        print('Doc failed', info)
                actions.clear()

    for success, info in helpers.parallel_bulk(es, actions, thread_count=1000):
        if not success:
            print('Doc failed', info)





if __name__ == '__main__':
    # read_file()
    dir()
