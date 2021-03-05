#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

../../Kafka/bin/zookeeper-server-stop.sh
tput setaf 001
if [[ $? -ne 0 ]]; then
	echo "Failed to shut Zookeeper down."
else
	echo "Zookeeper server DOWN."
fi
tput sgr0

../../Kafka/bin/kafka-server-stop.sh

tput setaf 001
if [[ $? -ne 0 ]]; then
	echo "Failed to shut Kafka server down."
else
	echo "Kafka server DOWN."
fi
tput sgr0
