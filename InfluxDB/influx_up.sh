#!/bin/bash

echo -n "Adding influx/influxd to \$PATH..."
sudo cp influxdb2-2.0.4-amd64/{influx,influxd} /usr/local/bin && echo "SUCCESS" || echo "FAILED"

echo -n "Installing .deb file..."
sudo dpkg -i influxdb2_2.0.4-amd64.deb && echo "SUCCESS" || echo "FAILED"

echo -n "Starting InfluxDB..."
sudo service influxdb start && echo "SUCCESS" || echo "FAILED"


