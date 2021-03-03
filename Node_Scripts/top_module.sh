#!/bin/bash

# This script is the top module for node-base script workflow
# Step 1: Install all dependencies
# Step 2: Start srsLTE & send metrics to Kafka


############################ GLOBALS ##########################
# Set variables
read -p "What is this node? (EPC/eNB/UE): " NODE_TYPE
# Convert to lower-case
NODE_TYPE=$(echo "${NODE_TYPE}"|tr '[A-Z]' '[a-z]')

############################ Step 1 ###########################

sudo apt-get update
sudo apt-get install default-jre -y

############################ Step 2 ###########################
case ${NODE_TYPE} in
	"epc")
		sudo ./epc_start
		;;
	"ue")
		sudo ./srslte_start ue
		;;
	"enb")
		sudo ./srslte_start enb
		;;
esac
