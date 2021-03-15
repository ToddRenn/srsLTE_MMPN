#!/bin/python3

import re
import time
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup InfluxDB parameters
token = "gIDHwTgATjZcwUjUkdwhl5xCAs0YvxXQ3-FWaOYPOIPC074pekVBZx7C3qrKczea1h5M_Ua1uJpFH1qCGOusYQ=="
org = "MMPN"
bucket = "TEST2"

# Initialize client and WRITE/DELETE APIs
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write = client.write_api(write_options=SYNCHRONOUS)
del_client = client.delete_api()
query_api = client.query_api()


value="enb1"


def query(bucket,value):
    res=query_api.query('from(bucket: "'+bucket+'") |> range(start: -60m) |> filter(fn: (r) => r["_field"] == "Name" and r["_value"] == "'+value+'")')
    for table in res:
        for row in table:
            rlist=[row.fields]
        first=rlist[0]
        return first['_field']
val = query(bucket,value)
print(val)
