#!/usr/bin/python3

from kafka import KafkaConsumer
import sys
import reader as rd

KAF_IP = sys.argv[2]
TOPIC = sys.argv[1]

consumer = KafkaConsumer(bootstrap_servers=[KAF_IP], value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)

for msg in consumer:
    if "log" in TOPIC:
        node=TOPIC.replace('_log','')
        rd.log_reader(msg.value,node)
    elif "csv" in TOPIC:
        node=TOPIC.replace('_log','')
        rd.csv_reader(msg.value,node)
    else:
        print("Incompatible file type.")
