#!/usr/bin/env python
# This script requires Python 2.6 or higher.

from __future__ import print_function, with_statement
import os
import sys
import subprocess
import re

_exec_cache = {}

def execute(cmd, cache=False):
    global _exec_cache
    if cache and cmd in _exec_cache:
        return _exec_cache[cmd]
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]
        if cache:
            _exec_cache[cmd] = result
        return result
    except:
        return None


def find_iface_node(name):
    ifnode = -1
    num_nodes = int(execute('cat /proc/cpuinfo | grep \'physical id\' | sort -u | wc -l'))
    for line in execute('ethtool -i {0}'.format(name), cache=True).splitlines():
        if line.startswith('bus-info:'):
            bus_location = line.split(':', 1)[1].strip()
            p1, p2, _ = bus_location.split(':')
            bus_prefix = '{0}:{1:02x}'.format(p1, int(p2, 16) & 0xf0)
            bus_affinity = execute('cat /sys/devices/pci{0}/pci_bus/{0}/cpuaffinity'.format(bus_prefix), cache=True).strip()
            for node in range(num_nodes):
                node_affinity = execute('cat /sys/devices/system/node/node{0}/cpumap'.format(node), cache=True).strip()
                if node_affinity == bus_affinity:
                    ifnode = node
                    break
    if ifnode == -1:
        ifnode = 0
    print('%s is on cpu node %d' %(name, ifnode))
    return ifnode


if __name__ == '__main__':

    #if os.geteuid() != 0:
    #    print('You must be root!', file=sys.stderr)
    #    sys.exit(1)
    ifname = sys.argv[1]
    node = find_iface_node(ifname)
    sys.exit(node)

