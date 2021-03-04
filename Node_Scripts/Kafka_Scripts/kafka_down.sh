#!/bin/bash

BASE="/proj/MMPN/groups/PG0/srsLTE_MMPN"

${BASE}/Kafka/bin/zookeeper-server-stop.sh
echo "ZooKeeper server terminated successfully."
${BASE}/Kafka/bin/kafka-server-stop.sh
echo "Kafka server terminated successfully."
