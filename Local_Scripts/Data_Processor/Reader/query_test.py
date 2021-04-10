#!/bin/python3

# This script generates InfluxDB entries from Kafka topics

import re, time
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup InfluxDB parameters
token = "7gKzElGkZUscd1EXz33HtAsDbUMAFovIYJcLpvCcwEowaTeAv8Gr4N5th0x8XHpA3TJ011eZ3hWeZepU6U669g=="
org = "MMPN"
bucket = "srsLTE"
url = "http://155.98.39.10:8086"

# Initialize client and WRITE/DELETE APIs
client = InfluxDBClient(url=url, token=token, org=org)
write = client.write_api(write_options=SYNCHRONOUS)
del_client = client.delete_api()
query_api = client.query_api()

def query_info(bucket, field,  value):
    q = query_api.query_stream('from(bucket: "'+bucket+'") |> range(start: -60d) \
                               |> filter(fn: (r) => r["_field"] == "'+field+'") \
                               |> filter(fn: (r) => r["_value"] == "'+value+'")')
    rlist=set()
    for record in q:
        rlist.add(record.get_measurement())
    return rlist

result=query_info('srsLTE','IP','172.16.0.2')
r_str=",".join(result)
arg='_measurement="'+r_str+'"'
time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
print(arg)
print(time)
del_client.delete('1970-01-01T00:00:00Z',time,arg,bucket,org)
