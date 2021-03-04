#!/usr/bin/python3

from kafka import KafkaConsumer
import sys
import reader as rd

KAF_IP='155.98.36.89:9092'
TOPIC=sys.argv[1]

consumer = KafkaConsumer(bootstrap_servers=[KAF_IP],
        auto_offset_reset="earliest",
        value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)
    
for msg in consumer:
	if "log" in TOPIC:
    	rd.log_reader(msg.value,TOPIC)
    elif "csv" in TOPIC:
    	rd.csv_reader(msg.value,TOPIC)
    else:
    	print("Can't read this file-type.")
