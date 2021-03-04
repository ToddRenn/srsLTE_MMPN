#!/bin/bash

# This node-based script starts a UE/eNB in srsLTE
# Step 1: Read in DL/UL center frequencies
# Step 2: Edit .conf files depending on UE/eNB selection - freq + metrics
# Step 3: Obtain Kafka information/set node identifiers
# Step 4: Start srsLTE and send data to Kafka

############################ Cleanup ###########################
pkill -x srsenb
pkill -x srsue
rm srslte_log 2> /dev/null

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

# Set metrics - period = 1 second
sed -ie 's/\#metrics_csv_e.*/metrics_csv_enable=true/' ${FILE_CONF}
sed -ie 's/\#metrics_p.*/metrics_period_secs=1/' ${FILE_CONF}

############################ Step 3 ############################
read -p "Kafka server IP: " KAF_IP
read -p "Node identifier: " NODE_ID
topicName="${NODE_ID}_log"

############################ Step 4 ############################
server="--bootstrap-server ${KAF_IP}:9092"
topic="--topic ${topicName}"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic} ${server}"
sudo srs${1} &> ${topicName} | tee ${kaf_cmd}

# If UE, then send the ue_metrics.csv
if [[ ${1} -eq "ue" ]]; then
	topic="--topic ${NODE_ID}_csv"
	kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic} ${server}"
	tail -f -n0 /tmp/ue_metrics.csv | ${kaf_cmd}
fi