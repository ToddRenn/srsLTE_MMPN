#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

../../Kafka/bin/zookeeper-server-stop.sh
tput setaf 001
echo "Zookeeper server DOWN."
tput sgr0

../../Kafka/bin/kafka-server-stop.sh

tput setaf 001
echo "Kafka server DOWN."
tput sgr0
