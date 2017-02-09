#!/usr/bin/env python
#coding=utf-8
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

ufw='{"ufw":{"allow":["192.168.10.15","192.168.10.2"],"deny":["192.168.10.13"]}}'

def run_cmd(cmd):
    print("###CMD : %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate()[0][:-1]


def ssh2(ip, username, passwd, cmd):
    import paramiko
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


def get_host(file):
    if not os.path.isfile(file):
        print("Configuration file does not exist\n")
        sys.exit(1)
    host = []
    peer = ""
    with open(file, 'r') as f:
        for c in f.readlines():
            if c.startswith('#'): continue
            host.append(c.strip('\n'))
            peer += c.strip('\n') + ","
    return peer[:-1]


def get_cpu():
    cpu_num = 0
    cmd = "lscpu | grep '^CPU(s)'"
    ret = run_cmd(cmd)

    num = int(ret.split()[1])
    print("###CPU NUMS: %d" % num)
    return num

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return


def conf_mongodb(cur_ip):
    with open("%s/mongo.conf" % (MONGODB_DIR), "w") as f:
        f.write("dbpath=%s/data/\n" % MONGODB_DATA)
    return


def main():
    for ip in host:
        ssh2(ip, USER, PASSWD, cmd)
    return

if __name__ == '__main__':
    main()
