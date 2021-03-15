#!/bin/bash
parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

# This runs all consumers
echo -ne "(1) RAST\n(2) InfluxDB\n"
read -p "Enter Choice #: " CHOICE
read -p "Kafka Server IP: " KAF_IP
topics=$(../../Kafka/bin/kafka-topics.sh --list --bootstrap-server ${KAF_IP}:9092)

for topic in ${topics}
do
	# Exclude the __consumer__metrics empty topic
	if [[ ${topic} != *"consumer"* ]]; then
		read -p "[TOPIC: ${topic}]Location: " LOC
		gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ${topic} ${KAF_IP} ${LOC} ${CHOICE}; exec bash"
	fi
done
