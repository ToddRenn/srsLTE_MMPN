#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

read -p "Include InfluxDB (y/n)? " ANS

# Update & Install Java
sudo apt-get update
sudo apt-get install default-jre -y

if [[ ${ANS} = "y" ]]
then
	# Install/configure InfluxDB
	echo -n "Adding influx/influxd to \$PATH..."
	sudo cp ../InfluxDB/influxdb2-2.0.4-linux-amd64/{influx,influxd} \
		/usr/local/bin && echo "SUCCESS" || echo "FAILED"
	echo -n "Installing .deb file..."
	sudo dpkg -i ../InfluxDB/influxdb2-2.0.4-amd64.deb && \
		echo "SUCCESS" || echo "FAILED"
	echo -n "Starting InfluxDB..."
	sudo service influxdb start && echo "SUCCESS" || echo "FAILED"
fi

