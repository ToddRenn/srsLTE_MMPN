#!/bin/bash

# This script creates a fake sensor that updates every
# user-defined period of time.

# Functions
update_csv(){
	# This function generates a CSV for a single sensor.
	# There are only 2 fields, and the name of the sensor
	# is determined from $NAME
	
	# Set variables
	MIN=0
	MAX=100
	VAL1=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL2=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL3=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL4=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL5=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL6=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL7=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	VAL8=$((MIN+RANDOM%(MAX-MIN))).$((RANDOM%99))
	
	# Update CSV (data rows are overwritten)
	echo -e "cc;rsrp;pl;cfo;mcs;snr;turbo;brate">>fake_sensor.csv

	for i in {1..10}
	do
		echo -e "${VAL1};${VAL2};${VAL3};${VAL4};${VAL5};${VAL6};${VAL7};${VAL8}">>fake_sensor.csv
	done
}


# Infinite loop which runs processes concurrently
while :
do
	tput setaf 4
	echo "Updating CSV..."
	tput sgr0
	update_csv
	sleep 0.001
done
