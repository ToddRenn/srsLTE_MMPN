#!/bin/bash

# This script starts a Kafka Cluster
# Step 1: Obtain the node public IP
# Step 2: Edit the server.properties file
# Step 3: Fire up ZooKeeper
# Step 4: Fire up Kafka Cluster

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

############################ Variables #########################
CFG_FILE="../../Kafka/config/server.properties"

############################ Step 1 ############################
PID_Kaf=$(ps ax | grep server.properties | grep -v grep | awk '{print $1}')
PID_Zoo=$(ps ax | grep zookeeper.properties | grep -v grep | awk '{print $1}')
if ps ax | grep server.properties | grep -v grep > /dev/null
then
	echo "Kafka already up. PID: ${PID_Kaf}"
	if ps ax | grep zookeeper.properties | grep -v grep > /dev/null
	then
		echo "Zookeeper already up. PID: ${PID_Zoo}"
	fi
	exit 1
fi

NODE_IP=$(ifconfig eno1 | grep -Po 'inet \K[\d.]+')
for x in {0..5}; do
	tput setaf $(( 255 - ${x}*4 ))
	echo "#################################"
done
tput setaf 201
echo "Kafka Server IP: ${NODE_IP}"
for x in {0..5}; do
	tput setaf $(( 240 + ${x}*4 ))
	echo "#################################"
done

tput sgr0

############################ Step 2 ############################
echo "Changing server.properties..."
sed -i "s/^advertised.l.*/advertised.listeners=PLAINTEXT:\/\/${NODE_IP}:9092/" \
	 ${CFG_FILE}
sed -i "s/^zookeeper.connect=[0-9].*/zookeeper.connect=localhost:2181/" \
	 ${CFG_FILE}


############################ Step 3 ############################
pid_checker() 'zookeeper' 'zookeeper'

############################ Step 4 ############################
pid_checker() 'kafka' 'server'

pid_checker()
{
	sudo ../../Kafka/bin/${1}-server-start.sh -daemon ../../Kafka/config/${2}.properties > /dev/null 2>&1
	tput setaf 040
	echo "Starting ${1}..."
	tput sgr0
	
	CHECK=1
	cnt=$(shuf -i 0-255 -n 1)
	while [ ${CHECK} -eq 1 ]; do
		tput setaf ${cnt}
        	echo -n "."
        	sleep 0.5
		ps ax | grep ${1}.properties | grep -v grep > /dev/null
		CHECK=$?
		if [[ ${cnt} -eq 0 ]]; then
			cnt=255
		else
			(( cnt-- ))
		fi
	done
	perl -e 'print "\xE2\x9C\x94 \xE2\x9C\x94 \xE2\x9C\x94 \xE2\x9C\x94"'
	echo ""
	tput setaf 111
	echo "${1} server UP."
	tput sgr0
}
