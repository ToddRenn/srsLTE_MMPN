#!/bin/bash

for pid in $(ps ax|grep python3|grep -v grep|awk '{print $1}'); do
    sudo kill -9 $pid
    echo "Killing $pid"
done
