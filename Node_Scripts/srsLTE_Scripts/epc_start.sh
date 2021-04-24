#!/bin/bash
# This script starts EPC and sends the output to a Kafka server

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

# Step 0: Cleanup
pkill -x srsepc

# Step 1: Obtain Kafka server IP and set node identifier (for topic)
read -p "Kafka IP is: " KAF_IP
read -p "Node identifier: " NODE_ID

topicName="${NODE_ID}_log"

# Step 2: Run srsEPC and send the output to a Kafka topic
server="--bootstrap-server ${KAF_IP}:9092"
topic="--topic ${topicName}"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic} ${server}"
sudo srsepc 2>&1 | ${kaf_cmd} 2> /dev/null &
