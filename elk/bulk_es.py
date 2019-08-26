#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

g_index = 'dev'
g_count = 3000
g_threadcount = 10

# es = Elasticsearch(hosts='http://elasticsearch', port=9400)
es = Elasticsearch(hosts='http://192.168.48.154', port=9400)


def opt(argv):
    global g_index
    global g_count
    global g_threadcount

    try:
        opts, args = getopt.getopt(argv[1:], "hi:c:t:", ["index=", "count="])
    except getopt.GetoptError:
        print(argv[0] + "-i <index prefix> -c <bulk count>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + "-i <index prefix> -c <bulk count>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            g_index = arg
        elif opt in ("-o", "--ofile"):
            g_count = int(arg)
        elif opt in "-t":
            g_threadcount = int(arg)

    print('index prefix: ' + g_index + ', bulk count: ' + str(g_count) + ', thread count: ' + str(g_threadcount))


def read_json(path):
    with open(path, 'r') as f:
        load_dict = json.load(f)
        # print(load_dict)
        # print(json.dumps(load_dict, indent=2))
    return load_dict


def bulk():
    actions = []
    json_obj = read_json('./access.json')

    for i in range(g_count):
        json_obj['@timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        action = {'_op_type': 'index',
                  '_index': g_index + '-' + datetime.now().strftime("%Y.%m.%d"),
                  '_type': 'doc',
                  '_source': json_obj}
        actions.append(action)

    for success, info in helpers.parallel_bulk(es, actions, thread_count=g_threadcount):
        if not success:
            print('Doc failed', info)


def main(argv):
    opt(argv)

    start_ts = int(time.time() * 1000)
    for i in range(10000):
        bulk()
        count = (i + 1) * g_count
        print(str(datetime.now()) + ' -> complete bulk count:', count, 'rate:',  1000 * (count / (time.time() * 1000 - start_ts)))


if __name__ == '__main__':
    # try:
    #     main(sys.argv)
    # except KeyboardInterrupt as e:
    #     print("KeyboardInterrupt")


    for i in range(256):
        print("wget -T 1 -t 1 192.168.12.%d" % i)
