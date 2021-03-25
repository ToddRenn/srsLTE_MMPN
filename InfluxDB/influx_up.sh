#!/bin/bash

echo "Adding influx/influxd to \$PATH..."
sudo cp influxdb2-2.0.4-linux-amd64/{influx,influxd} /usr/local/bin && echo -n "SUCCESS" || echo -n "FAILED"

echo "Installing .deb file..."
sudo dpkg -i influxdb2_2.0.4-amd64.deb && echo -n "SUCCESS" || echo -n "FAILED"

echo "Starting InfluxDB..."
sudo service influxdb start && echo -n "SUCCESS" || echo -n "FAILED"


