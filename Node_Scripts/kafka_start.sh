#!/bin/bash

# This script starts a producer for Apache Kafka
# Step 1: Read in the Kafka server IP
# Step 2: Ensure this is set in /etc/hosts
# Step 3: Extract NODE_ID which is the first IP octet
# Step 4: Set producer config properties
# Step 5: Start transmission of metrics

############################ Variables #########################
HOST_FILE="/etc/hosts"
KAF_FILE="/proj/mmpn-PG1/Kafka"

############################ Step 1 ############################
read -p "Kafka Server IP: " KAF_IP

############################ Step 2 ############################
grep -q "${KAF_IP}" ${HOST_FILE} \
  || echo -e "${KAF_IP} \t DESKTOP-B04CIKU" >> ${HOST_FILE}

############################ Step 3 ############################
IFS='.' read -a NODE_ID <<< $(hostname)

############################ Step 4 ############################
sed -i "s/^bootsrap.*/bootstrap.servers=${KAF_IP}:9092/" \
  ${KAF_FILE}/config/producer.properties

############################ Step 5 ############################
tail -f -n0 srslte.log | \
  ${KAF_FILE}/bin/kafka-console-producer.sh --topic ${NODE_ID}_log --bootstrap-server=${KAF_IP}:9092 &

if [[ ${1} -eq "ue" ]]; then
  tail -f -n0 /tmp/ue_metrics.csv | \
    ${KAF_FILE}/bin/kafka-console-producer.sh --topic ${NODE_ID}_metrics --bootstrap-server=${KAF_IP}:9092 &
fi
