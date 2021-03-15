#!/usr/bin/python3

from kafka import KafkaConsumer
import sys
import smac_reader as srdr
import csv_reader as crdr
import log_reader as lrdr

# Store arguments into variables
TOPIC = sys.argv[1]
KAF_IP = sys.argv[2]
LOC = sys.argv[3]
CHOICE = sys.argv[4]

# Initialize consumer for given topic
consumer = KafkaConsumer(bootstrap_servers=[KAF_IP], value_deserializer=lambda x: x.decode('utf-8'))
consumer.subscribe(TOPIC)

# Read in all consumer messages
for msg in consumer:
    if "log" in TOPIC:
        NODE_ID=TOPIC.replace('_log','')
        if CHOICE == "1":
            srdr.log_reader(msg.value,LOC,NODE_ID)
        else:
            lrdr.log_reader(msg.value,LOC,NODE_ID)
    elif "csv" in TOPIC:
        NODE_ID=TOPIC.replace('_csv','')
        if CHOICE == "1":
            srdr.csv_reader(msg.value,LOC,NODE_ID)
        else:
            crdr.csv_reader(msg.value,LOC,NODE_ID)
    else:
        print("Incompatible file type. Need logs/CSVs")
