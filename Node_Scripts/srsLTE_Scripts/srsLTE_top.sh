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
		sudo ./epc_start.sh
		;;
	"ue")
		sudo ./ue_start.sh
		;;
	"enb")
		sudo ./enb_start.sh
		;;
esac
