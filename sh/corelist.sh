#!/bin/sh

#var="1  2 3 4"
#echo $var | tr -cd ' ' | wc -c 
#exit
if [ $# -ne 1 ];
then
	echo ""
	echo "Help:"
	echo "$0 <proc name>"
	echo ""
	exit
fi
proc=$1
allpid=`pgrep $proc`
num=`pgrep $proc | wc -l`
#num=0
#for pid in $allpid
#do
	#echo $pid
#	num=$((num + 1))
#done

echo "procname [$proc] pidnum [$num]"

for pid in $allpid
do
	tid=`ls /proc/$pid/task`
	num=`echo $tid | tr -cd ' ' | wc -c`
	num=$((num + 1))
	echo ""
	echo "pid [$pid] has [$num] thread/task"
	for t in $tid
	do
		corelist=`taskset -pc $t | awk '{print $NF}'`
		if [ $t -eq $pid ]
		then
			echo "master thread [$t] working on core: [$corelist]"
		else
			echo "slaver thread [$t] working on core: [$corelist]"
		fi
	done
done
