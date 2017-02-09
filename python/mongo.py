#!/usr/bin/env python

import sys
import time
import json
import pymongo
from kafka import KafkaConsumer

def getMongoClientInstance():
    if 'mongoClientSingletonInstance' not in globals():
        globals()['mongoClientSingletonInstance'] = pymongo.MongoClient('mongo-rs0, mongo-rs1, mongo-rs2', 27017)
        return globals()['mongoClientSingletonInstance']
     
      
def insert_mongodb(mongo_client, db_name, collection_name, documents):
    try:
        #mongo_client[db_name][collection_name].insert_one(documents)
        print(documents)
    except pymongo.errors.AutoReconnect as e:
        pass

def main():
    mongo_client = getMongoClientInstance()
    consumer = KafkaConsumer('tcp', 'http', group_id='py-metadata',
                            auto_commit_enable=True,
                            auto_commit_interval_ms=10 * 1000,
                            auto_commit_interval_messages = 1000,
                            auto_offset_reset='smallest',
                            bootstrap_servers=['kafka-node0:9092','kafka-node1:9092','kafka-node2:9092'])
    
    while True:
        for message in consumer:
        #print(message.topic, message.partition, message.offset, message.value)
            if message is not None:
                topic = message.topic
                msg = json.loads(message.value)
                if (topic == 'tcp'):
                    insert_mongodb(mongo_client, "metadata", "tcp", msg)
                elif (topic == 'http'):
                    insert_mongodb(mongo_client, "metadata", "http", msg)
                else:
                    insert_mongodb(mongo_client, "metadata", "unknown", msg)
             
                consumer.task_done(message)


if __name__ == '__main__':
    main()
