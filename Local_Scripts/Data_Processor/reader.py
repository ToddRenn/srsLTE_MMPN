#!/usr/bin/python3

# This script takes file(s) as arguments, extracts info from the data
# and interfaces with SMAC accordingly.

import csv
import os
import sys
import time
import json
import requests
import re
from kafka import KafkaConsumer

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

def update_sensor(dict_list,topic):
    url = 'http://localhost:9091'
    smac_file="Output_Files/"+topic+".json"
    for data in dict_list:
        print(data)
        with  open(smac_file,"w") as json_file:
            json_file.write(str(data).strip("[]")+"SYSTEMMONITOR_COMMANDER_TRANSMISSION_COMPLETE")
        with  open(smac_file) as payload:
            r=requests.post(url, data=payload)

def log_reader(log,node,topic):
    # This function takes as input a string from a log file as well as the
    # topic it comes from (in order to create unique sensor names). The string
    # is parsed for KEY/VALUE pairs from which JSON commands are generated
    # log: Input string
    # topic: Topic name/identifier
    match_dict = dict() # Dictionary of matches
    ue_rx = []          # List of UE REGEX
    enb_rx = []         # List of eNB REGEx
    epc_rx = []         # List of EPC REGEX
    ues = set()         # Set of active UEs
    results = []        # List of SMAC-customized dictionaries

    #UE Filters
    ue_rx.append(re.compile(r'''
                   (?P<key>(type|clock_rate|EARFCN|f_dl|f_ul|Mode|PCI|PRB|CFO|c-rnti))[=]
                   (?P<value>-?[.\d\w]+)''', re.VERBOSE))

    ue_rx.append(re.compile(r'''
                   (?P<key>IP)[:\s]+
                   (?P<value>[.\d]+)''', re.VERBOSE))
    #eNB Filters
    enb_rx.append(re.compile(r'''
                        (?P<key>type|clock_rate|DL|UL)[=]
                        (?P<value>[.\d\w]+)''', re.VERBOSE))
    #EPC Filters
    epc_rx.append(re.compile(r'''
                        (?P<key>MCC|MNC|Name|id|PLMN|TAC|S1-U Address)[:]\s+
                        (?P<value>[.\d\w]+)''', re.VERBOSE))
    epc_rx.append(re.compile(r'''
                        (?P<key>IMSI)[:]\s+
                        (?P<value>[\d]{15})''', re.VERBOSE))
    epc_rx.append(re.compile(r'''
                        (?P<key>^Detach)[^\d]+
                        (?P<value>\d+)''', re.VERBOSE))
    epc_rx.append(re.compile(r'''
                        (?P<key>^Deleting eNB)[^\d]+
                        (?P<value>[\d\w]+)''', re.VERBOSE))
    
    # Use if/elif blocks to minimize REGEX analysis/line
    if "ue" in topic:
        for rx in ue_rx:
            for m in rx.finditer(log):
                match_dict[topic+"_"+m.group('key')]=m.group('value')
    elif "enb" in topic:
        for rx in enb_rx:
            for m in rx.finditer(log):
                match_dict[topic+"_"+m.group('key')]=m.group('value')
        if "connected" in log:
            x=log.split()
            ues.add(x[1])           # Stores a UE which connected to eNB
        if "Disconnecting" in log:
            s=log.split('=')
            ue_id=s[1].strip(".\n")
            if ue_id in ues:
                ues.remove(ue_id)   # Removes a UE which disconnected from eNB
    elif "epc" in topic:
        for rx in epc_rx:
            for m in rx.finditer(log):
                if m.group('key') == "IMSI":
                    ues.add(m.group('value'))   # Stores active UE IMSI
                elif m.group('key') == "Detach":
                    if m.group('value') in ues:
                        ues.remove(m.group('value'))# Removes inactive UE IMSI
                else:
                    match_dict[topic+"_"+m.group('key')]=m.group('value')
    # Create JSON objects from KEY/VALUE pairs
    for key in match_dict:
        results.append(custom_dict(key,match_dict.get(key),data, node))
    # Send off to SMAC
    update_sensor(results,topic)
    match_dict.clear()

def csv_reader(csv_in,node,topic):
    # This function reads in a CSV string, matches it with expected headers,
    # and creates a custom dictionary which represents the JSON SMAC command
    # csv_in: The CSV input string
    # topic: The name of the consumer topic it's coming from
    header=['time','rsrp','pl','cfo','dl_mcs','dl_snr','dl_turbo','dl_brate','dl_bler',\
            'ul_ta','ul_mcs','ul_buff','ul_brate','ul_bler','rf_o','rf_u','rf_l','is_attached']
    s = csv_in.split(";")
    s[len(s)-1]=s[len(s)-1].strip('\n') # Get rid of the newline from last
    metrics={}                          # The list of KEY/VALUE dictionaries
    dict_list = []                      # The list of SMAC JSON objects
    
    # Create our key/value pairs - skip the first column: time
    for i in range(1,len(header)):
        header[i] = topic+"_"+header[i]     # Custom SMAC sensor name
        metrics[header[i]] = s[i]       # Create/update the dictionary
    # Create custom JSON objects
    for key in metrics:
        dict_list.append(custom_dict(str(key),str(metrics.get(key)),data, node))
    # Send them off to SMAC
    update_sensor(dict_list,topic)
    dict_list.clear()

def custom_dict(key, value, data_dict, node):
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
    elif any(x in key for x in ['ul_buff','bsr']):
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
    elif any(x in key for x in ['DL','UL','f_ul','f_dl']):
        custom_dict["units"] = "Megahertz";
        custom_dict["type"] = "Double";
        custom_dict["minval"] = 0
        custom_dict["maxval"] = 10000
    elif "CFO" in key:
        custom_dict["units"] = "None";
        custom_dict["type"] = "String";
        custom_dict["minval"] = 0
        custom_dict["maxval"] = 10000
        custom_dict["value"] = value + "kHz"
    elif any(x in key for x in ['EARFCN','PRB']):
        custom_dict["units"] = "None";
        custom_dict["type"] = "Int";
        custom_dict["minval"] = 0
        custom_dict["maxval"] = 10000
    else:
        custom_dict["units"] = "None";
        custom_dict["type"] = "String";
        del custom_dict["minval"]
        del custom_dict["maxval"]

    return custom_dict

