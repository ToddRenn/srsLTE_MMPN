#!/bin/bash

# This script creates a topic on the node Kafka server
parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

read -a topicName -p "DELETE: Enter topic name(s): "
NODE_IP=$(ifconfig eno1 | grep -Po 'inet \K[\d.]+')

for name in "${topicName[@]}"; do
	echo "Deleting topic: "${name}
	../../Kafka/bin/kafka-topics.sh --delete --topic ${name} --bootstrap-server ${NODE_IP}:9092
done
