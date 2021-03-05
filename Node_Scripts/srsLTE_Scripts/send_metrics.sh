#!/bin/bash
read -p "Node ID: " NODE_ID
read -p "Kaf server: " server

topic_csv="--topic ${NODE_ID}_csv"
kaf_cmd="../../Kafka/bin/kafka-console-producer.sh ${topic_csv} ${server}"
tail -f -n0 /tmp/ue_metrics.csv | ${kaf_cmd} &
