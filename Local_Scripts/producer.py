#!/usr/bin/python3

# Args: File to send through Kafka Server
import sys
from kafka import KafkaProducer
bootstrap_servers = ['155.98.36.76:9092']
topic = 'weeeee'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
message = open(sys.argv[1],"r")
for line in message:
    ack = producer.send(topic, line.encode('utf-8'))
    metadata = ack.get()
    print(str(metadata.topic)+str(metadata.partition))
