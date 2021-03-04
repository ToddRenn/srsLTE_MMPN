#!/bin/bash

# This script is the top module for srsLTE

BASE="/proj/MMPN/groups/PG0/Node_Scripts/srsLTE_Scripts"
BASE_UE="/proj/mmpn-PG0/groups/srsLTE_MMPN/Node_Scripts/srsLTE_Scripts"
############################ GLOBALS ##########################
# Set variables
read -p "What is this node? (EPC/eNB/UE): " NODE_TYPE
# Convert to lower-case
NODE_TYPE=$(echo "${NODE_TYPE}"|tr '[A-Z]' '[a-z]')

############################ Step 1 ###########################
case ${NODE_TYPE} in
	"epc")
		sudo ./Node_Scripts/srsLTE_Scripts/epc_start.sh
		;;
	"ue")
		sudo ./Node_Scripts/srsLTE_Scripts/srslte_start.sh ue
		;;
	"enb")
		sudo ./Node_Scripts/srsLTE_Scripts/srslte_start.sh enb
		;;
esac
