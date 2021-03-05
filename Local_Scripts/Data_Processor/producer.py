#!/usr/bin/python3

# Args: File to send through Kafka Server
import sys, time
from kafka import KafkaProducer

server = ['155.98.37.211:9092']
topic='ue1_csv'

producer = KafkaProducer(bootstrap_servers=server)
#producer = KafkaProducer(value_serialization=lambda x: x.encode('utf-8'))

while True:
	with open("Output_Files/ue_metrics.csv","rt") as logfile:
		for line in logfile:
			ack = producer.send(topic, line.encode('utf-8'))
			metadata = ack.get()
			print(line,end='')
			time.sleep(1)
