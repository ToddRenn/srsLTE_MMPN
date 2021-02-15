#!/bin/bash

# This node-based script starts a UE/eNB in srsLTE
# Step 1: Read in DL/UL center frequencies
# Step 2: Edit .conf files depending on UE/eNB selection - freq + metrics
# Step 3: Start srsLTE

############################ Cleanup ###########################
pkill -x srsepc
pkill -x srsenb
pkill -x srsue
rm srslte.log 2> /dev/null

############################ Step 1 ############################
# Set variables
read -p "DL Center Frequency: " DL_FREQ
read -p "UL Center Frequency: " UL_FREQ
FILE_CONF="/etc/srslte/${1}.conf"

# Ensure frequencies are in MHz
if [[ "$DL_FREQ" != *"e6" ]]; then
  DL_FREQ=${DL_FREQ}e6;
fi
if [[ "$UL_FREQ" != *"e6" ]]; then
  UL_FREQ=${UL_FREQ}e6;
fi

############################ Step 2 ############################
# Comment out dl_earfcn
sed -ie '/^dl_ear.*/ s/./#&/' ${FILE_CONF}

# Change dl_freq in the file
sed -i '/^dl_freq.*/d' ${FILE_CONF}
sed -ie "s/^\[rf\]/\[rf\]\ndl_freq=${DL_FREQ}/" ${FILE_CONF}

# Change dl_freq in the file
sed -i '/^ul_freq.*/d' ${FILE_CONF}
sed -ie "s/^\[rf\]/\[rf\]\nul_freq=${UL_FREQ}/" ${FILE_CONF}

# Set metrics - period = 0.1 seconds
sed -ie 's/\#metrics_csv_e.*/metrics_csv_enable=true/' ${FILE_CONF}
sed -ie 's/\#metrics_p.*/metrics_period_secs=0.1/' ${FILE_CONF}

############################ Step 3 ############################
srs${1} &> srslte.log &
