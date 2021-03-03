#!/usr/bin/python3

# Args: File to send through Kafka Server
import sys
from kafka import KafkaProducer
bootstrap_servers = ['155.98.36.89:9092']
topic='One'

KafkaProducer(bootstrap_servers=bootstrap_servers,
              'One',value_serialization=lambda x: x.encode('utf-8'))
#ack = producer.send(topic, line.encode('utf-8'))
#metadata = ack.get()
#print(str(metadata.topic)+str(metadata.partition))
