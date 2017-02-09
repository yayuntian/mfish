#!/bin/sh
sed -e '/export KAFKA_HEAP_OPTS/a\    export JMX_PORT=9999' /usr/kafka_2.10-0.8.2.1/bin/kafka-server-start.sh


echo "delete.topic.enable=true" >> server.properties


