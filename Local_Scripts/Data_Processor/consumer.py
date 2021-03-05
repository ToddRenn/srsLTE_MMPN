#!/usr/bin/python3

from kafka import KafkaConsumer
import sys
import reader as rd

TOPIC = sys.argv[1]
KAF_IP = sys.argv[2]
node = sys.argv[3]

consumer = KafkaConsumer(bootstrap_servers=[KAF_IP], value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)

for msg in consumer:
    if "log" in TOPIC:
        node_name=TOPIC.replace('_log','')
        rd.log_reader(msg.value,node,node_name)
    elif "csv" in TOPIC:
        node_name=TOPIC.replace('_log','')
        rd.csv_reader(msg.value,node,node_name)
    else:
        print("Incompatible file type.")
