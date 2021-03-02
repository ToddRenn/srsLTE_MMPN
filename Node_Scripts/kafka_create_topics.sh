#!/bin/bash

# This script creates a topic on the node Kafka server

read -a topicName -p "Enter topic name(s): "
NODE_IP=$(ifconfig eno1 | grep -Po 'inet \K[\d.]+')

for name in "${topicName[@]}"; do
	echo("Creating topic: "${name})
	../Kafka/bin/kafka-topics.sh --create --topic ${name} --bootstrap-server ${NODE_IP}:9092
