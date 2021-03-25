#!/usr/bin/python3

# Args: File to send through Kafka Server
import sys, time
from kafka import KafkaProducer

server = ['155.98.36.47:9092']
topic=sys.argv[1]
f=sys.argv[2]
producer = KafkaProducer(bootstrap_servers=server)

while True:
    with open("Output_Files/"+f,"rt") as logfile:
        for line in logfile:
            ack = producer.send(topic, line.encode('utf-8'))
            metadata = ack.get()
            print(line,end="")
            time.sleep(0.1)
