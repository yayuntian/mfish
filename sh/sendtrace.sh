#!/bin/bash
trap "echo Exit!; exit;" SIGINT SIGTERM

while [ 1 ]
do
	cat $1 | while read line
	do
		echo $line
		sudo /home/nfs/yayun/sh/tcpreplay -i eth2 -M 20 $line > /dev/null 2>&1
	done
done
