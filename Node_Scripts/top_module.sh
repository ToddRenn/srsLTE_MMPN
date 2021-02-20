#!/bin/bash

# This script is the top module for node-base script workflow
# Step 1: Start srslte
# Step 2: Start Kafka & Transmit data

############################ GLOBALS ##########################
# Set variables
read -p "What is this node? (EPC/eNB/UE): " NODE_TYPE
# Convert to lower-case
NODE_TYPE=$(echo "${NODE_TYPE}"|tr '[A-Z]' '[a-z]')

############################ Step 1 ###########################
sudo ./srslte_start.sh ${NODE_TYPE}
# Wait until UE fully setup...
(tail -f -n0 srslte.log &)|grep -q 'Searching'

############################ Step 2 ###########################
sudo ./kafka_start.sh ${NODE_TYPE}
