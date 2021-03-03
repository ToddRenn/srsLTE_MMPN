#!/usr/bin/python3

# This script takes file(s) as arguments, extracts info from the data
# and interfaces with SMAC accordingly.

import csv
import os
import subprocess
import sys
import time
import json
import requests
from kafka import KafkaConsumer

def tail(thefile):
    thefile.seek(0,2) # Look at last line of thefile

    while not thefile.closed:   # Continue running until file is closed
        line = thefile.readline()
        if not line:            # If no new line is written, wait
            time.sleep(5)
            continue
        #if line and line.endswith('\n') # If line is written AND it's complete
        yield line

def update_sensor(dict_list):
    url = 'http://localhost:9091'
    for data in dict_list:
        json_file = open(sys.argv[1]+".json","w")
        json_file.write(str(data).strip("[]")+"SYSTEMMONITOR_COMMANDER_TRANSMISSION_COMPLETE")
        json_file.close()
        #payload = open("sensor.json")
        #r=requests.post(url, data=payload)
def log_reader(filename):
    log = tail(open(filename,"rt"))
    
    #UE Filters
    
    #eNB Filters

    #EPC Filters

def csv_reader(filename):
    metrics = csv.DictReader(tail(open(filename,"rt")), delimiter=';')
    dict_list = []
    data = {
            "hostname": "localhost",
            "portnum": 9091,
            "minval": 0.0,
            "system": "true",
            "version": "2.4",
            "units": "Celsius",
            "type": "Double",
            "forceEnable": "true",
            "maxval": 100.0,
            "sensor": "",
            "value": 0,
            "command": "update-sensor",
            "timeout": 5
            }

    for row in metrics:
        for key in row.keys():
            dict_list.append(custom_dict(str(key),str(row.get(key)),data))
        update_sensor(dict_list[1:])
        dict_list.clear()

def custom_dict(key, value, data_dict):
    custom_dict = data_dict.copy()
    custom_dict["sensor"] = key;
    custom_dict["value"] = value;
    
    if "rsrp" in key:
        custom_dict["units"] = "dBm";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = -140;
        custom_dict["maxval"] = -44;
    elif "pl" in key:
        custom_dict["units"] = "dBm";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 0;
        custom_dict["maxval"] = 100;
    elif "cfo" in key:
        custom_dict["units"] = "Hertz";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 0;
        custom_dict["maxval"] = 1000000000;
    elif "mcs" in key:
        custom_dict["units"] = "None";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 0.00;
        custom_dict["maxval"] = 28.00;
    elif "brate" in key:
        custom_dict["units"] = "bps";
        custom_dict["type"] = "String";
        del custom_dict["minval"]
        del custom_dict["maxval"]
    elif "bler" in key:
        custom_dict["units"] = "Percent";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 0.00;
        custom_dict["maxval"] = 100.00;
    elif "snr" in key:
        custom_dict["units"] = "dBm";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 1.00;
        custom_dict["maxval"] = 30.00;
    elif "ul_buff" in key or "bsr" in key:
        custom_dict["units"] = "Bytes";
        custom_dict["type"] = "String";
        del custom_dict["minval"]
        del custom_dict["maxval"]
    elif "ul_ta" in key:
        # Note: SMAC doesn't have a microsecond unit, modify value
        custom_dict["units"] = "Milliseconds";
        custom_dict["type"] = "Int";
        custom_dict["minval"] = 0;
        custom_dict["maxval"] = 63;
    elif "attached" in key:
        if value == "1.0":
            custom_dict["value"] = "Yes"
        else:
            custom_dict["value"] = "No"
        custom_dict["units"] = "None";
        custom_dict["type"] = "String";
        del custom_dict["minval"]
        del custom_dict["maxval"]
    else:
        custom_dict["units"] = "None";
        custom_dict["type"] = "String";
        del custom_dict["minval"]
        del custom_dict["maxval"]

      return custom_dict

if __name__ == '__main__':
    if "csv" in sys.argv[1]:
        csv_reader(sys.argv[1])
    else:
        print('log_reader')
