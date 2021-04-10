#!/bin/bash

# This script tails the metrics at a given POWDER node
# and stores the file locally as ${NODE_TYPE}_metrics.csv
# NOTE: Make sure metric recording is ENABLED on the nodes.
parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"
cnt=$(shuf -i 0-255 -n 1)
while read p; do
	tput setaf ${cnt}
        echo "$p"
        sleep 0.07
	(( cnt-- ))
done < ../Node_Scripts/srsLTE_Scripts/mmpn.txt
tput sgr0

# Read/Declare vars
read -p "POWDER username: " UNAME
ADDR_UE=()
ADDR_ENB=()

# Set PC# & location for Kafka server
read -p "Kafka Server PC#: " KAFKA_PC
read -p "Kafka PC location (MEB/Fort): " DATA_CTR
DATA_CTR=$(echo "${DATA_CTR}"|tr '[A-Z]' '[a-z]')

if [[ "${DATA_CTR}" == "fort" ]]; then
	ADDR_KAF="${UNAME}@pc${KAFKA_PC}-fort.emulab.net"
else
	ADDR_KAF="${UNAME}@pc${KAFKA_PC}-meb.emulab.net"
fi

# Set PC# & location for srsLTE nodes
read -a PC -p "Experiment PC #(s): "
for PC in "${PC[@]}"; do
  read -p "Experiment PC#${PC} location (MEB/Fort): " DATA_CTR
  DATA_CTR=$(echo "${DATA_CTR}"|tr '[A-Z]' '[a-z]')

  if [[ "${DATA_CTR}" == "fort" ]]; then
    ADDR_ENB+=( "${UNAME}@pc${PC}-fort.emulab.net" )
  else
    ADDR_ENB+=( "${UNAME}@pc${PC}.emulab.net" )
  fi
done

read -a LOC -p "UE location(s): "
for LOC in "${LOC[@]}"; do
  ADDR_UE+=( "${UNAME}@nuc2.${LOC}.powderwireless.net" )
done



# MAIN

# ################### STEP 0; Kill past srsLTE processes ######################
ssh -p22 ${ADDR_ENB} 'sudo pkill -x srsepc; sudo pkill -x srsenb'
ssh -p22 ${ADDR_UE} 'sudo pkill -x srsue'

# ################### STEP 1: Start srsLTE ####################################
for ADDRS in "${ADDR_ENB[@]}"; do
  # Step 1.1 Start EPC
  tput setaf 6
  echo "Connecting to EPC at ${ADDRS}..."
  tput sgr0
  gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDRS}; exec bash"

  # Step 1.2 Start eNB
  tput setaf 6
  echo "Connecting to eNB at ${ADDRS}..."
  tput sgr0
  gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDRS} -Y; exec bash"
done

for ADDRS in "${ADDR_UE[@]}"; do
  # Step 1.3 Start UE
  tput setaf 6
  echo "Connecting to UE at ${ADDRS}..."
  tput sgr0
  gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDRS} -Y; exec bash"
done
# ################### STEP 2: Start Kafka Server ###############################
tput setaf 6
echo "Connecting to Kafka node at ${ADDR_KAF}"
tput sgr0
 gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDR_KAF}; exec bash"

