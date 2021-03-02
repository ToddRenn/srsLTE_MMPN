#!/usr/bin/python3

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'Todd_Test',
    bootstrap_servers=['136.60.139.186:9092'],
    value_deserializer=lambda x: x.decode('utf-8'))

filename = 'whatever.txt'

data = open(filename,"w")
for message in consumer:
    data.write(message.value)
    data.write("\n")
    #print("%s:%d:%d: key=%s value=%s" % (message.topic,message.partition,message.offset,message.key,message.value))
