#!/bin/bash

# This script tails the metrics at a given POWDER node
# and stores the file locally as ${NODE_TYPE}_metrics.csv
# NOTE: Make sure metric recording is ENABLED on the nodes.

# Read/Declare vars
read -p "POWDER username: " UNAME
read -p "Data Center (MEB/Fort): " DATA_CTR
DATA_CTR=$(echo "${DATA_CTR}"|tr '[A-Z]' '[a-z]')
read -a PC -p "PC #(s): "
read -a LOC -p "UE location(s): "

ADDR_UE=()
ADDR_ENB=()

for PC in "${PC[@]}"; do
  if [[ "${DATA_CTR}" -eq "fort" ]]; then
    ADDR_ENB+=( "${UNAME}@pc${PC}-fort.emulab.net" )
  else
    ADDR_ENB+=( "${UNAME}@pc${PC}.emulab.net" )
  fi
done

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
  gnome-terminal --tab -- bash -ic "ssh -p22 ${ADDRS} 'sudo srsepc'; exec bash"

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
