#!/bin/bash

# This script stops all background srsLTE and Kafka processes

############################ Cleanup ###########################
for pid in $(ps ax|grep srsenb|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done
for pid in $(ps ax|grep srsepc|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done
for pid in $(ps ax|grep srsue|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done
for pid in $(ps ax|grep ConsoleProducer|grep -v grep|awk '{print $1}'); do
	sudo kill -9 $pid
done
