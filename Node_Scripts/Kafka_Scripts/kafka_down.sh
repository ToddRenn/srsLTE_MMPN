#!/bin/bash

BASE="/proj/MMPN/groups/PG0/srsLTE_MMPN"

${BASE}/Kafka/bin/zookeeper-server-stop.sh

${BASE}/Kafka/bin/kafka-server-stop.sh
