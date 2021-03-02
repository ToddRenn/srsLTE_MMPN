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
        json_file = open("sensor.json","w")
        json_file.write(str(data).strip("[]")+"SYSTEMMONITOR_COMMANDER_TRANSMISSION_COMPLETE")
        json_file.close()
        payload = open("sensor.json")
        r=requests.post(url, data=payload)

def csv_reader(file):
    metrics = csv.DictReader(tail(open(file,"rt")), delimiter=';')
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
        update_sensor(dict_list)
        dict_list.clear()

def custom_dict(key, value, data_dict):
    #pseudo: if key is XXX, then create a custom copy
    custom_dict = data_dict.copy()
    custom_dict["sensor"] = key;
    custom_dict["value"] = value;

    switch(key) {
        case "rsrp":
            custom_dict["units"] = "dBm";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = -140;
            custom_dict["maxval"] = -44;
            break;
        case "pl":
            custom_dict["units"] = "dBm";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = 0;
            custom_dict["maxval"] = 100;
            break;
        case "cfo":
            custom_dict["units"] = "Hertz";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = 0;
            custom_dict["maxval"] = 1000000000;
            break;
        case "mcs":
        case "dl_mcs" :
        case "ul_mcs" :
            custom_dict["units"] = "None";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = 0.00;
            custom_dict["maxval"] = 28.00;
            break;
        case "brate":
        case "dl_brate" :
        case "ul_brate" :
            custom_dict["units"] = "bps";
            custom_dict["type"] = "String";
            del custom_dict["minval"]
            del custom_dict["maxval"]
            break;
        case "bler":
        case "dl_bler" :
        case "ul_bler" :
            custom_dict["units"] = "Percent";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = 0.00;
            custom_dict["maxval"] = 100.00;
            break;
        case "snr":
        case "dl_snr" :
        case "ul_snr" :
            custom_dict["units"] = "dBm";
            custom_dict["type"] = "Double";
            custom_dict["minval"] = 1.00;
            custom_dict["maxval"] = 30.00;
            break;
        case "ul_buff":
        case "bsr" :
            custom_dict["units"] = "Bytes";
            custom_dict["type"] = "String";
            del custom_dict["minval"]
            del custom_dict["maxval"]
            break;
        case "ul_ta":
            # Note: SMAC doesn't have a microsecond unit, modify value
            custom_dict["units"] = "Milliseconds";
            custom_dict["type"] = "Int";
            custom_dict["minval"] = 0;
            custom_dict["maxval"] = 63;
            break;
        case "turbo":
            custom_dict["units"] = "None";
            custom_dict["type"] = "String";
            del custom_dict["minval"]
            del custom_dict["maxval"]
            break;

    }

    return custom_dict

def file_creator(topicName):
   consumer = KafkaConsumer(
                    topicName,
                    bootstrap_servers=['136.60.139.186:9092'],
                    value_deserializer=lambda x: x.decode('utf-8'))
   
   filename = topicName+'.data'
   data = open(filename,"w")

   for message in consumer:
       data.write(message.value)

   if "ue" in topicName:
       ue_csv_reader(filename)
   elif "enb" in topicName:
       enb_reader(filename)
   else:
       epc_reader(filename)

if __name__ == '__main__':
    # loop through all arguments - excluding script call (argv[0])
    for arg in sys.argv[1:]:
        file_creator(arg)
