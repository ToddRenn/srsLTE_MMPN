#!/usr/bin/python3

from kafka import KafkaConsumer
import sys

KAF_IP='155.98.36.89:9092'
TOPIC=sys.argv[1]
file_path="Output_Files/"+TOPIC

consumer = KafkaConsumer(bootstrap_servers=[KAF_IP],
        auto_offset_reset="earliest",
        value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)


f = open(file_path, "w", buffering=1)
    
for msg in consumer:
    f.write(msg.value)
    f.write("\n")
