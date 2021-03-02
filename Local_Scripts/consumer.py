#!/usr/bin/python3

from kafka import KafkaConsumer

# Files
ue_csv_file =


ue_csv_consumer = KafkaConsumer(
    'ue_metrics',
    bootstrap_servers=['155.98.36.76:9092'],
    group_id='UE',
    auto_offset_reset="earliest",
    value_deserializer=lambda x: x.decode('utf-8'))

#print(consumer.topics())
for message in ue_csv_consumer:
    #data.write(message.value)
    #data.write("\n")
    #print("%s:%d:%d: key=%s value=%s" % (message.topic,message.partition,message.offset,message.key,message.value))
    print(message.value)
