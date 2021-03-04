#!/usr/bin/python3

# This script takes file(s) as arguments, extracts info from the data
# and interfaces with SMAC accordingly.

import csv
import os
import sys
import time
import json
import concurrent.futures
import requests
import re
from kafka import KafkaConsumer

node_name = re.match(r'''.*[/](\w*)''',sys.argv[1]).group(1)
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

def tail(filename):
    #thefile.seek(0,2) # Look at last line of thefile
    while True:   # Continue running until file is closed
        thefile = open(filename,"r")
        line = thefile.readline()
        thefile.close()
        if not line:            # If no new line is written, wait
            time.sleep(1)
            continue
        yield line

def update_sensor(dict_list):
    url = 'http://localhost:9091'
    for data in dict_list:
        json_file = open(node_name+".json","a")
        json_file.write(str(data).strip("[]")+"SYSTEMMONITOR_COMMANDER_TRANSMISSION_COMPLETE")
        json_file.close()
        #payload = open("sensor.json")
        #r=requests.post(url, data=payload)

def log_reader(filename):
    def log_tailer(filename):
        yield tail(filename)
    
    with concurrent.futures.ThreadPoolExecutor() as ex:
        f = ex.submit(log_tailer, filename)
        log  = f.result()
    print("we are after thread declaration")
    print(log)
    match_dict = dict()# Dictionary of matches
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
    # Scan through file
    for line in log:
        if "ue" in filename:
            for rx in ue_rx:
                for m in rx.finditer(line):
                    match_dict[node_name+"_"+m.group('key')]=m.group('value')
        elif "enb" in filename:
            for rx in enb_rx:
                for m in rx.finditer(line):
                    match_dict[node_name+"_"+m.group('key')]=m.group('value')
            if "connected" in line:
                x=line.split()
                ues.add(x[1])
            if "Disconnecting" in line:
                s=line.split('=')
                ue_id=s[1].strip(".\n")
                if ue_id in ues:
                    ues.remove(ue_id)
        elif "epc" in filename:
            for rx in epc_rx:
                for m in rx.finditer(line):
                    if m.group('key') == "IMSI":
                        ues.add(m.group('value'))
                    elif m.group('key') == "Detach":
                        ues.remove(m.group('value'))
                    else:
                        match_dict[node_name+"_"+m.group('key')]=m.group('value')
    for key in match_dict:
        results.append(custom_dict(key,match_dict.get(key),data))
    update_sensor(results)
    match_dict.clear()

def csv_reader(filename):
    def csv_tailer(filename):
        return csv.DictReader(tail(open(filename,"rt")), delimiter=';')
    
    with concurrent.futures.ThreadPoolExecutor() as ex:
        f = ex.submit(csv_tailer, filename)
        metrics  = f.result()
    t1 = threading.Thread(target=csv_tailer,args=filename)
    t1.start()
    print("we here boyz")
    dict_list = []

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

if __name__ == '__main__':
    if "csv" in sys.argv[1]:
        csv_reader(sys.argv[1])
    else:
        log_reader(sys.argv[1])

