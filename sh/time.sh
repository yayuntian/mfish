#!/bin/sh


echo "nameserver 218.2.135.1" > /etc/resolv.conf
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ntpdate cn.pool.ntp.org
timedatectl set-timezone Asia/Shanghai
timedatectl set-local-rtc yes
