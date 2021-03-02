#!/usr/bin/python3

from kafka import KafkaProducer
bootstrap_servers = ['136.60.139.186:9092']
topic = 'Todd_Test'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

for e in range(10):
    message = "Message #" + str(e)
    ack = producer.send(topic, message.encode('utf-8'))
    metadata = ack.get()
    print(str(metadata.topic)+str(metadata.partition))
