#!/usr/bin/env python

import sys
import os
import re
import fcntl
import paramiko
import threading
import socket
import struct
import getopt
import subprocess

PERFIX = '/tmp/'
VERSION = 'saas-0.1-alphal'


PACKET = [ "tar xvf /root/%s/jdk-8u45-linux-x64.tar.gz -C %s" % (VERSION, PERFIX),
"tar xvf /root/%s/kafka_2.10-0.8.2.1.tgz -C %s" % (VERSION, PERFIX),
"tar xvf /root/%s/hadoop-2.7.1.tar.gz -C %s" % (VERSION, PERFIX),
"tar xvf /root/%s/kafka-manager-1.2.8.tgz -C %s" % (VERSION, PERFIX),
"tar xvf /root/%s/spark-1.4.1-bin-hadoop2.6.tgz -C %s" % (VERSION, PERFIX),
"mv /root/%s/spark-streaming-kafka-assembly_2.10-1.4.1.jar /%s/spark-1.4.1-bin-hadoop2.6/" % (VERSION, PERFIX)
]


usage = '''Important:
    1) You must copy DCS installation package to peers /root dir
    2) You must specify a Host file, the file containing the peers IP
Usage:
    -i  install 
    -h  get a usage summary
Examples:
    ./install.py -i hostfile
'''

USER = 'root'
PASSWD = '123456'

def run_cmd(cmd):
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    return p.communicate()[0][:-1]

def get_ip(ifname='eth2'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])

def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        print "### Host:%s Output Str Start\n" % ip
        for m in cmd:
            print "## Cmd: ", m
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.read()
            if out: print(out[:-1])
            err = stderr.read()
            if err: print(err[:-1])
        ssh.close()
    except Exception,e:
        print "\n%s\tError ,reason is : %s" % (ip, str(e))
    print "\n### Host:%s Output Str End\n" % ip

def unpack(peer):
    cmd = []
    print('### Unpack and Install ......')
    xcmd = "tar xvf /root/%s.tgz -C /root" % VERSION
    cmd.append(xcmd)
    cmd.extend(PACKET)

    print(cmd)

    for ip in peer:
        ssh2(ip, USER, PASSWD, cmd)
    


def main():
    try:
        opts, args=getopt.getopt(sys.argv[1:], "i:h", ["help"])
        if not opts:
            print("Welcome to ClearClouds SAAS Toolkit")
            print("Copyright(c) 2015 ClearClouds Technology (Wuxi) Co., Ltd")
            print('')
            print('Use -h to get a usage summary')
            sys.exit()
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    host = []
    for o,a in opts:
        if o == '-i':
            peer = a
        elif o in ("-h", "--help"):
            print(usage)
            sys.exit()
        else:
            assert False, "unhandled option"
    if not peer:
        print("unhandled option\nplease input one correct peers file")
        sys.exit()
    with open(peer, 'r') as f:
        for c in f.readlines():
            if c.startswith('#'): continue
            host.append(c.strip('\n'))
        print("This Operation Other Peers: %s\n" % host)

    unpack(host)

if __name__ == '__main__':
    main()
