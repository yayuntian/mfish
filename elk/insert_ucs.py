#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts='http://localhost', port=9200)


def do_es_ts(timestr):
    tm = time.strptime(timestr, "%Y-%m-%dT%H:%M:%S+08:00")
    ts = time.mktime(tm)
    other_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # print(other_time)
    return other_time



def read_json():
    count = 0
    actions = []
    with open('/Users/eric/Downloads/ucs-bug/ucs-all/ucs-27.json', 'r') as f:
        for line in f:
            # print(line)
            source = json.loads(line)
            try:
                sp = source['message'].split(",")
                source['version'] = sp[10].split("=")[1]
                source['platformid'] = sp[21].split("=")[1]
                source['device_id'] = sp[24].split("=")[1]
                source['ua'] = sp[27].split("=")[1][:-1]
            except:
                print(line)

            count = count + 1
            action = {'_op_type': 'index',
                      '_index': 'ucs-log-2019-10-28',
                      '_type': 'doc',
                      '_source': source}
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


def read_file():
    count = 0
    actions = []
    with open('/Users/eric/Downloads/ucs-bug/ucs.log', 'r') as f:
        for line in f:
            print(line.split("\""))
            sp = line.split("\"")
            tmp = dict()
            tmp["ip"] = sp[0].split(" ")[0]
            tmp["@timestamp"] = do_es_ts(sp[0].split(" ")[3][1:-1])
            tmp["url"] = sp[1][4:]
            # tmp["url"] = sp[5]
            # tmp["version"] = sp[6][:-1]
            tmp["status"] = int(sp[3])
            tmp["byte"] = int(sp[4].strip())
            tmp["refer"] = sp[7]
            tmp["ua"] = sp[9]

            tmp["duration"] = float(sp[11])
            tmp["host"] = sp[13]
            tmp["port"] = int(sp[15])
            print(count, json.dumps(tmp, indent=2))
            # print(count, tmp["duration"])
            count = count +1

            action = {'_op_type': 'index',
                      '_index': 'ucs-2019-10-29',
                      '_type': 'doc',
                      '_source': tmp}
            actions.append(action)
            # print(count)


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
    read_json()
