#!/bin/bash
trap "echo Exit!; exit;" SIGINT SIGTERM

while :
do
    for f in /home/gaoju/gaoju/dianping_tracefile/dianping.pcap3*
    do 
        echo $f
        sudo /home/nfs/yayun/sh/tcpreplay -i eth2 -M 20 $f > /dev/null 2>&1
    done
done
