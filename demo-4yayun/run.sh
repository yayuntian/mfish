#!/usr/bin/env bash
echo "start tcpdump"
nohup tcpdump -i any -G 600  -w /tmp/debug-%Y%m%d_%H%M_%S.pcap &
echo "start jar"
java $JAVA_OPTS -jar /tomcat/demo.jar
