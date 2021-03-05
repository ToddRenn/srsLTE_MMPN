#!/bin/bash
parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

# This runs all consumers
read -p "Kafka Server IP: " KAF_IP
topics=$(../../Kafka/bin/kafka-topics.sh --list --bootstrap-server ${KAF_IP}:9092)

for topic in ${topics}
do
	# Exclude the __consumer__metrics empty topic
	if [[ ${topic} != *"consumer"* ]]; then
		read -p "[TOPIC: ${topic}]Node hostname: " NODE_NAME
		gnome-terminal --tab -- bash -ic "python3 consumer.py ${topic} ${KAF_IP} ${NODE_NAME}; exec bas"
	fi
done
