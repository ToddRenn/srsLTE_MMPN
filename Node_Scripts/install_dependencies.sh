#!/bin/bash

parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
cd "${parent}"

# Update & Install Java
sudo apt-get update
sudo apt-get install default-jre -y

# Install/configure InfluxDB
echo -n "Adding influx/influxd to \$PATH..."
sudo cp ../InfluxDB/influxdb2-2.0.4-linux-amd64/{influx,influxd} \
	/usr/local/bin && echo "SUCCESS" || echo "FAILED"
echo -n "Installing .deb file..."
sudo dpkg -i ../InfluxDBinfluxdb2-2.0.4-amd64.deb && \
	echo "SUCCESS" || echo "FAILED"
echo -n "Starting InfluxDB..."
sudo service influxdb start && echo "SUCCESS" || echo "FAILED"


