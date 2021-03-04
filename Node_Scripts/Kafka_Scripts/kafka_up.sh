#!/bin/bash

# This script starts a Kafka Cluster
# Step 1: Obtain the node public IP
# Step 2: Edit the server.properties file
# Step 3: Fire up ZooKeeper
# Step 4: Fire up Kafka Cluster

############################ Variables #########################
BASE="/proj/MMPN/groups/PG0/srsLTE_MMPN"
CFG_FILE="${BASE}/Kafka/config/server.properties"


############################ Step 1 ############################
NODE_IP=$(ifconfig eno1 | grep -Po 'inet \K[\d.]+')
echo "Kafka Server IP: ${NODE_IP}"

############################ Step 2 ############################
echo "Changing server.properties..."
sed -i "s/^advertised.l.*/advertised.listeners=PLAINTEXT:\/\/${NODE_IP}:9092/" \
	 ${CFG_FILE}
sed -i "s/^zookeeper.connect=[0-9].*/zookeeper.connect=localhost:2181/" \
	 ${CFG_FILE}


############################ Step 3 ############################
${BASE}/Kafka/bin/zookeeper-server-start.sh -daemon ${BASE}/Kafka/config/zookeeper.properties

############################ Step 4 ############################
${BASE}/Kafka/bin/kafka-server-start.sh -daemon ${BASE}/Kafka/config/server.properties
