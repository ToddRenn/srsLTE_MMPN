#!/bin/bash

# This node-based script starts a UE in srsLTE
# Step 1: Read in DL/UL center frequencies
# Step 2: Edit .conf files depending on UE/eNB selection - freq + metrics
# Step 3: Obtain Kafka information/set node identifiers
# Step 4: Start srsLTE and send data to Kafka

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

############################ Cleanup ###########################
for pid in $(ps ax|grep srsue|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done
for pid in $(ps ax|grep ConsoleProducer|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done

############################ Step 1 ############################
# Set variables

read -p "DL Center Frequency: " DL_FREQ
read -p "UL Center Frequency: " UL_FREQ
FILE_CONF="/etc/srslte/ue.conf"

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
echo "Topic name:${topicName}"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic} ${server}"
tput setaf 111
echo "Sending ${NODE_ID} log files... "
tput sgr0
sudo srsue 2>&1 | ${kaf_cmd} 2> /dev/null &

# Send the ue_metrics.csv
sleep 45
tput setaf 111
echo "Sending ${NODE_ID} metrics..."
tput sgr0
topic_csv="--topic ${NODE_ID}_csv"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic_csv} ${server}"
tail -f -n0 /tmp/ue_metrics.csv | ${kaf_cmd} 2> /dev/null &
