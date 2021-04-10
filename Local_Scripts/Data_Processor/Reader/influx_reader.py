#!/bin/python3

# This script generates InfluxDB entries from Kafka topics

import re, time
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup InfluxDB parameters
token = "13Ygwlo1m4qfpobAL9HMHyfQqh-nhlKDq-Vls3pum4c66qwyjkKBad758rX8a_btVWek3GiiVV1jpRWNixuDBA=="
org = "MMPN"
bucket = "srsLTE"

# Initialize client and WRITE/DELETE APIs
client = InfluxDBClient(url="http://155.98.37.201:8086", token=token)
write = client.write_api(write_options=SYNCHRONOUS)
del_client = client.delete_api()
query_api = client.query_api()

def init_influx_dict(NODE_ID,LOC):
    # This function initializes an entry in the global
    # dictionaries with all definitions necessary
    # for an InfluxDB dictionary entry
    dict_list={}
    dict_list['measurement']=NODE_ID
    dict_list['tags']={}
    dict_list['tags']['Location']=LOC
    dict_list['fields']={}
    #dict_list['time']=str(datetime.utcnow())
    return dict_list

def update_actives(dict_list,LOC,choice,NODE_ID):
    global bucket, org
    #time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    if choice == 'Add':
        influx_entry={}
        influx_entry['measurement'] = NODE_ID
        influx_entry['tags'] = {}
        influx_entry['tags']['Status'] = 'Active'
        influx_entry['fields'] = dict_list
        #influx_entry['time'] = time
        print(str(influx_entry))
        write.write(bucket,org,influx_entry)
        #write.close()
    elif choice == 'Delete':
        arg='_measurement="'+NODE_ID+'"'
        del_client.delete('1970-01-01T00:00:00Z',time,arg,bucket=bucket,org=org)
    else:
        return

def query_info(bucket, field,  value):
    rlist=set()
    q = query_api.query_stream('from(bucket: "'+bucket+'") \
                    |> range(start: -60d) \
                    |> filter(fn: (r) => r["_field"] == "'+field+'" \
                    and r["_value"] == "'+value+'")')
    for record in q:
        rlist.add(record.get_measurement())
    return rlist
