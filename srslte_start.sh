#!/bin/bash

# This node-based script starts a UE/eNB in srsLTE
# Step 1: Read in DL/UL center frequencies
# Step 2: Edit .conf files depending on UE/eNB selection - freq + metrics
# Step 3: Start srsLTE

############################ Step 1 ############################
# Set variables
read -p "What is this node? (UE/eNB): " NODE_TYPE
read -p "DL Center Frequency: " DL_FREQ
read -p "UL Center Frequency: " UL_FREQ
FILE_CONF="/etc/srslte/${NODE_TYPE}.conf"

# Convert to lower-case
NODE_TYPE=$(echo "$NODE_TYPE"|tr '[A-Z]' '[a-z]')

# Ensure frequencies are in MHz
if [[ "$DL_FREQ" != *"e6" ]]; then
  DL_FREQ=${DL_FREQ}e6;
fi
if [[ "$UL_FREQ" != *"e6" ]]; then
  UL_FREQ=${UL_FREQ}e6;
fi

############################ Step 2 ############################
# Comment out dl_earfcn
sudo sed -ie '/^dl_ear.*/ s/./#&/' ${FILE_CONF}

# Change dl_freq in the file
sudo grep -q '^dl_freq' ${FILE_CONF} \
  && sudo sed -i 's/^dl_freq/dl_freq=${DL_FREQ}/' ${FILE_CONF} \
  || sudo sed -ie 's/\[rf\]/\[rf\]\ndl_freq=${DL_FREQ}/' ${FILE_CONF}

# Change dl_freq in the file
sudo grep -q '^ul_freq' ${FILE_CONF} \
  && sudo sed -i 's/^ul_freq/ul_freq=${UL_FREQ}/' ${FILE_CONF} \
  || sudo sed -ie 's/\[rf\]/\[rf\]\ndl_freq=${UL_FREQ}/' ${FILE_CONF}

# Set metrics - period = 0.1 seconds
sudo sed -ie 's/\#metrics_csv_e.*/metrics_csv_enable=true' ${FILE_CONF}
sudo sed -ie 's/\#metrics_p.*/metrics_period_secs=0.1' ${FILE_CONF}

############################ Step 3 ############################
sudo srs${NODE_TYPE} &> srslte.log
