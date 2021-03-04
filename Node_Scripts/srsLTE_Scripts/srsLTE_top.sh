#!/bin/bash

# This script is the top module for srsLTE


############################ GLOBALS ##########################
# Set variables
read -p "What is this node? (EPC/eNB/UE): " NODE_TYPE
# Convert to lower-case
NODE_TYPE=$(echo "${NODE_TYPE}"|tr '[A-Z]' '[a-z]')

############################ Step 1 ###########################
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