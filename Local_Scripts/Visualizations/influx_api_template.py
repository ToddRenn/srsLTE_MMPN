#!/bin/python3
import re
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS

# Setup basic parameters
token = "gIDHwTgATjZcwUjUkdwhl5xCAs0YvxXQ3-FWaOYPOIPC074pekVBZx7C3qrKczea1h5M_Ua1uJpFH1qCGOusYQ=="
org = "MMPN"
bucket = "TEST"
client = InfluxDBClient(url="http://localhost:8086", token=token)
write = client.write_api(write_options=SYNCHRONOUS)
del_client = client.delete_api()
del_client.delete('1970-01-01T00:00:00Z','2021-04-27T00:00:00Z','_measurement=ue2',bucket=bucket,org=org)
# Global dictionaries

ues={} #Global dictionary for UE

def csv_reader(csv_in,node,topic):
    # This function reads in a CSV string, matches it with expected headers,
    # and creates a custom dictionary which represents the JSON SMAC command
    # csv_in: The CSV input string
    # topic: The name of the consumer topic it's coming from
    if not node in ues:
        init_influx_dict(node)
    header=['time','rsrp','pl','cfo','dl_mcs','dl_snr','dl_turbo','dl_brate','dl_bler',\
            'ul_ta','ul_mcs','ul_buff','ul_brate','ul_bler','rf_o','rf_u','rf_l','is_attached']
    s = csv_in.split(";")
    s[len(s)-1]=s[len(s)-1].strip('\n') # Get rid of the newline from last
    metrics={}                          # The list of KEY/VALUE dictionaries
    metrics['measurement']=node
    time=datetime.utcnow()
    metrics['time']=str(time)
    fields={}

    # Create our key/value pairs - skip the first column: time
    for i in range(1,len(header)):
        if header[i] == 'is_attached':
            if s[i] == '1.0':
                fields[header[i]] = 'Yes'
            else:
                fields[header[i]] = 'No'
        else: 
            fields[header[i]] = float(s[i])       # Create/update the dictionary
    metrics['fields']=fields
    ues[node]=metrics
    write.write(bucket,org,metrics)
    write.close()

def init_influx_dict(node):
    # This function initializes an entry in the global
    # dictionaries with all definitions necessary
    # for an InfluxDB dictionary entry
    ues[node]={}
    ues[node]['measurement']=node
    ues[node]['tags']={}
    ues[node]['fields']={}
    ues[node]['time']=str(datetime.utcnow())

def log_reader(log,node,topic):
    # Initialize UE if not already present
    if not node in ues:
        init_influx_dict(node)
    
    # Variables
    ue_rx = []          # List of UE REGEX
    
    # Filters
    ue_rx.append(re.compile(r'''
                   (?P<key>(type|clock_rate|EARFCN|f_dl|f_ul|Mode|PCI|PRB|CFO|c-rnti))[=]
                   (?P<value>-?[.\d\w]+)''', re.VERBOSE))

    ue_rx.append(re.compile(r'''
                   (?P<key>IP|Device)[:\s]+
                   (?P<value>[.\d]+)''', re.VERBOSE))
    
    # Create tags from log file values
    for rx in ue_rx:
        for m in rx.finditer(log):
            ues[node]['tags'][m.group('key')]=m.group('value')
    
    # Update the timestamp
    ues[node]['time']=str(datetime.utcnow())
    print(ues[node])

if __name__=='__main__':
    csv=open('Output_Files/ue.log','rt')
    csv_in=csv.readlines()[1:]
    for line in csv_in:
        log_reader(line,"ue2","ue2")
#        print(ues)
