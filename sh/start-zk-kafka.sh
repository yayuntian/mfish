#!/bin/sh
nohup zookeeper-server-start.sh  /usr/kafka/kafka_2.10-0.8.2.1/config/zookeeper.properties &
sleep 5
nohup kafka-server-start.sh  /usr/kafka/kafka_2.10-0.8.2.1/config/server.properties &
