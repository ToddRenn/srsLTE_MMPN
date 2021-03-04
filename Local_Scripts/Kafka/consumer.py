#!/usr/bin/python3

from kafka import KafkaConsumer
import sys
import reader as rd

KAF_IP = srs.argv[2]
TOPIC = sys.argv[1]

consumer = KafkaConsumer(bootstrap_servers=[KAF_IP],
        auto_offset_reset="earliest",
        value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)
    
for msg in consumer:
	if "log" in TOPIC:
		node="${TOPIC\\_log\}"
    	rd.log_reader(msg.value,node)
    elif "csv" in TOPIC:
		node="${TOPIC\\_csv\}"
    	rd.csv_reader(msg.value,node)
    else:
    	print("Can't read this file-type.")
