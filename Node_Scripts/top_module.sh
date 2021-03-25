#!/bin/bash
# This script is the top module for srsLTE

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

############################ GLOBALS ##########################
# Set variables
read -p "What is this node? (EPC/eNB/UE): " NODE_TYPE
# Convert to lower-case
NODE_TYPE=$(echo "${NODE_TYPE}"|tr '[A-Z]' '[a-z]')

############################ Step 1 ###########################
case ${NODE_TYPE} in
	"epc")
		sudo srsLTE_Scripts/epc_start
		;;
	"ue")
		sudo srsLTE_Scripts/srslte_start ue
		;;
	"enb")
		sudo srsLTE_Scripts/srslte_start enb
		;;
esac
