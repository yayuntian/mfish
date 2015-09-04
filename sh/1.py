#!/usr/bin/env python

import sys
import os
import re
import fcntl
#import paramiko
import threading
import socket
import struct
import getopt
import subprocess

PERFIX = '/tmp/'
VERSION = 'saas-0.1-alphal'
ENV_FILE='/tmp/profile'


JDK_VERSION='jdk-8u45-linux-x64'
KAFKA_VERSION='kafka_2.10-0.8.2.1'
KAFKA_MANAGER_VERSION='kafka-manager-1.2.8'
SPARK_VERSION='spark-1.4.1-bin-hadoop2.6'
MONGODB_VERSION='mongodb-linux-x86_64-3.0.6'


KAFKA_DIR='/dfs/kafka-logs'
ZK_DIR='/dfs/zookeeper'
MONGODB_DIR='/dfs/mongodb/'


PACKET = [ "tar xvf /root/%s/%s.tar.gz -C %s" % (VERSION, JDK_VERSION, PERFIX),
"tar xvf /root/%s/%s.tgz -C %s" % (VERSION, KAFKA_VERSION, PERFIX),
"tar xvf /root/%s/%s.tgz -C %s" % (VERSION, KAFKA_MANAGER_VERSION, PERFIX),
"tar xvf /root/%s/%s.tgz -C %s" % (VERSION, SPARK_VERSION, PERFIX),
"mv /root/%s/spark-streaming-kafka-assembly_2.10-1.4.1.jar /%s/%s/" % (VERSION, PERFIX, SPARK_VERSION),
"tar xvf /root/%s/%s.tgz -C %s" % (VERSION, MONGODB_VERSION, PERFIX)
]

def run_cmd(cmd):
    print("###CMD : %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate()[0][:-1]

def get_cpu():
    cpu_num = 0
    cmd = "lscpu | grep '^CPU(s)'"
    ret = run_cmd(cmd)

    num = ret.split()[1]
    if cpu_num.isdigit():
        print("###CPU NUMS: %d" % num)
        cpu_num = num
    else:
        print("###CPU NUMS ERROR, USE DEFAULT")

    return cpu_num


def main():

    length = len(sys.argv)

    if length <= 1:
        print('Use ./install.py ipaddr1 ipaddr2 ipaddr3 ...')
        sys.exit()

    # get peer ip
    peer = []
    i = 1
    while ( i < length):
        peer.append(sys.argv[i])
        i += 1
    print("All Peers: %s\n" % peer)

    # get master ip && curret index/ip    
    context = run_cmd("ifconfig")
    for index, ip in enumerate(peer):
        if ip in context:
            break
    print("current ip: %s, index: %d" % (ip, index))

    master_ip = peer[0]
    cur_index = index
    cur_ip = ip

    # get zookeeper list    ex: host1:2181,host2:2181,host3:2181 ...
    text = ""
    for ip in peer:
        text += ip + ":2181,"
    zkhosts = text[:-1]

    # unpack all package
    cmd = PACKET
    for c in cmd:
        ret = run_cmd(c)

    # config os env
    cmd = []

    del_cmd = ["sed -i '/^export JAVA_HOME=/d' %s" % ENV_FILE,
        "sed -i '/^export JRE_HOME=/d' %s" % ENV_FILE,
        "sed -i '/^export CLASSPATH=/d' %s" % ENV_FILE,
        "sed -i '/^export KAFKA_HOME=/d' %s" % ENV_FILE,
        "sed -i '/^export SPARK_LOCAL_DIRS=/d' %s" % ENV_FILE,
        "sed -i '/^export MONGODB_HOME=/d' %s" % ENV_FILE,
        "sed -i '/^export PATH=/d' %s" % ENV_FILE
    ]


    add_cmd = ["echo 'export JAVA_HOME=%s' >> %s" % (PERFIX + JDK_VERSION, ENV_FILE),
        "echo 'export JRE_HOME=$JAVA_HOME/jre' >> %s" % ENV_FILE,
        "echo 'export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib' >> %s" % ENV_FILE,
        "echo 'export KAFKA_HOME=%s' >> %s" % (PERFIX + KAFKA_VERSION, ENV_FILE),
        "echo 'export SPARK_LOCAL_DIRS=%s' >> %s" % (PERFIX + SPARK_VERSION, ENV_FILE),
        "echo 'export MONGODB_HOME=%s' >> %s" % (PERFIX + MONGODB_VERSION, ENV_FILE),
        "echo 'export PATH=$PATH:$JAVA_HOME/bin:$KAFKA_HOME/bin:$MONGODB_HOME/bin' >> %s" % ENV_FILE
    ]

    cmd.extend(del_cmd)
    cmd.extend(add_cmd)

    for c in cmd:
        run_cmd(c)

    #config kafka

    cmd = [
        "sed -i '/export KAFKA_HEAP_OPTS/a\    export JMX_PORT=9999' %s/bin/kafka-server-start.sh" % (PERFIX + KAFKA_VERSION),
        "sed -i 's/^zookeeper.connect=/zookeeper.connect=%s/g' %s/config/server.properties" % (zkhosts, PERFIX + KAFKA_VERSION),
        "sed -i 's/^broker.id=[0-9]*/broker.id=%d/g' %s/config/server.properties" % (cur_index, PERFIX + KAFKA_VERSION),
        "sed -i '/^log.dirs=/d'  %s/config/server.properties" % (PERFIX + KAFKA_VERSION),
        "echo 'log.dirs=%s' >> %s/config/server.properties" % (KAFKA_DIR, PERFIX + KAFKA_VERSION),
        "echo 'delete.topic.enable=true' >> %s/config/server.properties" % (PERFIX + KAFKA_VERSION),
    ]

    cpus = get_cpu()
    if cpus != 0:
        cmd.append("sed -i 's/^num.network.threads=[0-9]*/num.network.threads=%d/g' %s/config/server.properties" % (cpus,PERFIX + KAFKA_VERSION))
        cmd.append("sed -i 's/^num.io.threads=[0-9]*/num.io.threads=%d/g' %s/config/server.properties" % (cpus * 2, PERFIX + KAFKA_VERSION))

    for c in cmd:
        run_cmd(c)

    # config zookeeper

    cmd = [
        "sed -i '/^dataDir=/d'  %s/config/zookeeper.properties" % (PERFIX + KAFKA_VERSION),
        "echo 'dataDir=%s' >> %s/config/zookeeper.properties" % (ZK_DIR, PERFIX + KAFKA_VERSION),
        "echo 'initLimit=5' >> %s/config/zookeeper.properties" % (PERFIX + KAFKA_VERSION),
        "echo 'syncLimit=5' >> %s/config/zookeeper.properties" % (PERFIX + KAFKA_VERSION)
    ]

    for index, ip in enumerate(peer):
        tmp = "server.%d=%s:2888:3888" % (index, ip)
        cmd.append("echo %s >> %s/config/zookeeper.properties" % (tmp, PERFIX + KAFKA_VERSION))

    cmd.append("echo %d > %s/myid" % (cur_index, ZK_DIR))

    for c in cmd:
        run_cmd(c)


    # config kafka-manager

    cmd = [
        "sed -i '/^kafka-manager.zkhosts=/d'  %s/conf/application.conf" % (PERFIX + KAFKA_MANAGER_VERSION),
        "echo kafka-manager.zkhosts=%s >> %s/conf/application.conf" % (zkhosts, PERFIX + KAFKA_MANAGER_VERSION)
    ]
    for c in cmd:
        run_cmd(c)

    # config spark

    with open("%s/conf/slaves" % (PERFIX + SPARK_VERSION), "w") as f:
        for index, ip in enumerate(peer):
            if index == 0 : continue
            f.write(ip)
    
    with open("%s/conf/spark-env.sh" % (PERFIX + SPARK_VERSION), "w") as f:
        f.wirte("export SPARK_MASTER_IP=%s" % master_ip)
        f.write("export JAVA_HOME=/usr/jdk1.8.0_45/")


    # config mongodb

    with open("%s/mongo.conf" % (PERFIX + MONGODB_VERSION), "w") as f:
        f.write("dbpath=%s/data/" % MONGODB_DIR)
        f.write("logpath=%s/log/mongodb.log" % MONGODB_DIR)
        f.write("pidfilepath=%s/mongodb.pid" % MONGODB_DIR)
        f.write("directoryperdb=true")
        f.write("logappend=true")
        f.write("replSet=testrs")
        f.write("bind_ip=%s" % cur_ip)
        f.write("port=27017")
        f.write("oplogSize=10000")
        f.write("fork=true")
        f.write("noprealloc=true")


if __name__ == '__main__':
    main()
