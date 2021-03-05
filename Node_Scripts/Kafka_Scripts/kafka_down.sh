#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

../../Kafka/bin/kafka-server-stop.sh

CHECK=0
while [ ${CHECK} -ne 1 ]; do
	tput setaf ${cnt}
        echo -n "."
        sleep 0.5
	ps ax | grep 'kafka\.Kafka ' | grep java | grep -v grep | awk '{print $1}'
	CHECK=$?
done
tput sgr0

tput setaf 001
if [[ $? -ne 0 ]]; then
	echo "Failed to shut Kafka server down."
else
	echo "Kafka server DOWN."
fi
tput sgr0

../../Kafka/bin/zookeeper-server-stop.sh
tput setaf 001
if [[ $? -ne 0 ]]; then
	echo "Failed to shut Zookeeper down."
else
	echo "Zookeeper server DOWN."
fi
tput sgr0
