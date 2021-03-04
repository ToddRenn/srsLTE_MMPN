#!/bin/bash

# This runs all consumers
#read -p "Kafka Server IP: " KAF_IP
KAF_IP='155.98.36.89:9092'
topics=$(../../Kafka/bin/kafka-topics.sh --list --bootstrap-server ${KAF_IP})
for topic in ${topics}
do
	# Exclude the __consumer__metrics empty topic
	if [[ ${topic} != *"consumer"* ]]; then
		python3 consumer.py ${topic} ${KAF_IP} &
	fi
done
