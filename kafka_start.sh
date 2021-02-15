#!/bin/bash

# This script starts a producer for Apache Kafka
# Step 1: Read in the Kafka server IP
# Step 2: Ensure this is set in /etc/hosts
# Step 3: Extract NODE_ID which is the first IP octet
# Step 4: Set producer config properties
# Step 5: Start transmission of metrics

############################ Variables #########################
FILE_PATH="/etc/hosts"
KAF_FILE="/proj/mmpn-pg1/Kafka"

############################ Step 1 ############################
read -p "Kafka Server IP: " KAF_IP

############################ Step 2 ############################
sudo grep -q '^${KAF_IP}' ${FILE_PATH} \
  || sudo echo -e "${KAF_IP} \t DESKTOP-B04CIKU" ${FILE_PATH}

############################ Step 3 ############################
IFS='.' read -a NODE_ID <<< $(hostname)

############################ Step 4 ############################
sudo sed -i 's/^bootsrap.*/bootstrap.servers=${KAF_IP}:9092' \
  ${KAF_FILE}/config/producer.properties

############################ Step 5 ############################
tail -f -n0 ~/srslte.log | \
  .${KAF_FILE}/bin/producer.sh --topic $NODE_ID --bootstrap-server=${KAF_IP}:9092
