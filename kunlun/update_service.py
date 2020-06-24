#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import json
import time
import requests

SleepTs = 20
ImageUrl = "yhub-public.ssl.ysten.com:8880/ycs/kunlun-docs:{}".format(os.getenv('IMG_TAG', 'latest'))
ServiceUrl = "https://kunlun.ssl.ysten.com/ysten-docker/service/wwjfiti4trclb36xlkab7q5r4"
ServiceJson = """
{
    "name": "kunlun-docs",
    "taskTemplate": {
        "containerSpec": {
            "image": "yhub-public.ssl.ysten.com:8880/ycs/kunlun-docs:0.1-3-g8f77981"
        },
        "resources": {
            "limits": {
                "cpus": 1,
                "memory": "512M"
            },
            "reservations": {
                "cpus": 0.1,
                "memory": "64M"
            }
        },
        "restartPolicy": {
            "condition": "on-failure",
            "delay": 10000000000,
            "maxAttempts": 5,
            "window": 1800000000000
        },
        "placement": {
            "constraints": [
                "node.role==worker",
                "node.labels.kunlun.node.default==default"
            ]
        },
        "logDriver": {
            "name": "json-file",
            "options": {
                "max-size": "100M",
                "max-file": 3
            }
        },
        "networks": [
            {
                "target": "ycs_net"
            }
        ],
        "forceUpdate": 0
    },
    "mode": {
        "replicated": {
            "replicas": 1
        }
    },
    "updateConfig": {
        "parallelism": 0,
        "failureAction": "continue",
        "order": "stop-first",
        "maxFailureRatio": 0
    },
    "endpointSpec": {
        "mode": "vip",
        "ports": [
            {
                "protocol": "tcp",
                "publishMode": "ingress",
                "publishedPort": 8887,
                "targetPort": 80
            }
        ]
    }
}
"""


def update():
    data = json.loads(ServiceJson)
    data['taskTemplate']['containerSpec']['image'] = ImageUrl
    print("update service image: {}".format(ImageUrl))

    headers = {'Content-Type': 'application/json',
               'X-Auth': 'dGlhbnlheXVuQHlzdGVuLmNvbTp5c3QwMzIw'}
    request = requests.put(ServiceUrl, json=data, headers=headers, timeout=3)
    return request.content


if __name__ == "__main__":
    print('sleep {}s waiting for image sync to yhub-public ...'.format(SleepTs))
    time.sleep(SleepTs)
    ret = update()
    print(ret)
