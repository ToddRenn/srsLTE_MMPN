#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

sudo ../../Kafka/bin/kafka-server-stop.sh
pid_checker() kafka

sudo ../../Kafka/bin/zookeeper-server-stop.sh
pid_checker() zookeeper

pid_checker()
{
	CHECK=0
	cnt=$(shuf -i 0-255 -n 1)
	while [ ${CHECK} -ne 1 ]; do
		tput setaf ${cnt}
        	echo -n "."
        	sleep 0.5
		ps ax | grep ${1}.properties | grep -v grep > /dev/null
		CHECK=$?
		if [[ ${cnt} -eq 0 ]]; then
			cnt=255
		else
			(( cnt-- ))
		fi
	done
	perl -e 'print "\xE2\x9C\x94 \xE2\x9C\x94 \xE2\x9C\x94 \xE2\x9C\x94"'
	echo ""
	tput setaf 001
	echo "${1} server DOWN."
	tput sgr0
}
