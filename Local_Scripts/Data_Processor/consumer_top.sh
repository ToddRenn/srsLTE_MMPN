#!/bin/bash

# This runs all consumers
read -p "Kafka Server IP: " KAF_IP
topics=$(./Kafka/bin/kafka-topics.sh --list --bootstrap-server ${KAF_IP}:9092)

for topic in ${topics}
do
	# Exclude the __consumer__metrics empty topic
	if [[ ${topic} != *"consumer"* ]]; then
		python3 Local_Scripts/Data_Processor/consumer.py ${topic} ${KAF_IP} &
	fi
done
