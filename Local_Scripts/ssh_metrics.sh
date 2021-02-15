#!/bin/bash

# This script tails the metrics at a given POWDER node
# and stores the file locally as ${NODE_TYPE}_metrics.csv
# NOTE: Make sure metric recording is ENABLED on the nodes.

# Read/Declare vars
read -p "POWDER username: " UNAME
read -a PC -p "PC #(s): "
read -a LOC -p "UE location(s): " LOC

ADDR_UE="${UNAME}@nuc2.${LOC}.powderwireless.net"
ADDR_ENB="${UNAME}@pc${PCNUM}-fort.emulab.net"
BASE_DIR="/proj/mmpn-PG0/"

# MAIN

# ################### STEP 0; Kill past srsLTE processes ######################
ssh -p22 ${ADDR_ENB} 'sudo pkill -x srsepc; sudo pkill -x srsenb'
ssh -p22 ${ADDR_UE} 'sudo pkill -x srsue'

# ################### STEP 1: Start srsLTE ####################################
# Step 1.1 Start EPC
tput setaf 6
echo "Connecting to EPC at ${ADDR_ENB}..."
tput sgr0
gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDR_ENB} 'sudo srsepc'; exec bash"

# Step 1.2 Start eNB
tput setaf 6
echo "Connecting to eNB at ${ADDR_ENB}..."
tput sgr0
gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDR_ENB} -Y 'cd ${BASE_DIR}'; exec bash"

# Step 1.3 Start UE
tput setaf 6
echo "Connecting to UE at ${ADDR_UE}..."
tput sgr0
gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDR_UE} -Y 'cd ${BASE_DIR}'; exec bash"
