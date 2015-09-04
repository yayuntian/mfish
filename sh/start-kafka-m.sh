#!/bin/sh
nohup /root/kafka-manager-1.2.8/bin/kafka-manager -Dconfig.file=/root/kafka-manager-1.2.8/conf/application.conf -Dhttp.port=8081 > ./km.log  2>&1 &
