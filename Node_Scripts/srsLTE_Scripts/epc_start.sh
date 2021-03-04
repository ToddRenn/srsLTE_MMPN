#!/bin/bash

# This script starts EPC and sends the output to a Kafka server

# Step 0: Cleanup
pkill -x srsepc

# Step 1: Obtain Kafka server IP and set node identifier (for topic)
read -p "Kafka server IP: " KAF_IP
read -p "Node identifier: " NODE_ID

topicName="${NODE_ID}_log"

# Step 2: Run srsEPC and send the output to a Kafka topic
server="--bootstrap-server ${KAF_IP}:9092"
topic="--topic ${topicName}"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic} ${server}"
sudo srsepc &> ${topicName} | tee ${kaf_cmd}
