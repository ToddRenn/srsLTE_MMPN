#!/usr/bin/python3

from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# Setup basic parameters
token = "gIDHwTgATjZcwUjUkdwhl5xCAs0YvxXQ3-FWaOYPOIPC074pekVBZx7C3qrKczea1h5M_Ua1uJpFH1qCGOusYQ=="
org = "MMPN"
bucket = "TEST"

# Setup objects
client = InfluxDBClient(url="http://localhost:8086", token=token)
del_client = client.delete_api()
# write options can set batch sizes so no need for .close() calls all
# the time. it'll automatically do this I think.
write_api = client.write_api(write_options=ASYNCHRONOUS)

del_client.delete('1970-01-01T00:00:00Z','2021-04-27T00:00:00Z','_measurement=ue1',bucket=bucket,org=org)
# Setup list of POINTS
pts=[Point("ue1")\
     .tag("location","hospital")\
     .tag("UL (MHz)",2505)\
     .tag("equipment","x310")\
     .field("bler %",20)\
     .field("pl",-40)\
     .time(datetime.utcnow(),WritePrecision.NS),
     Point("ue1")\
     .field("snr",3.5)]
#Point("point2").tag("location","helsinki").field("you okay?",False).time(datetime.utcnow(),WritePrecision.NS),
#Point("point3").tag("location","YMH").field("you okay?",1.0001).time(datetime.utcnow(),WritePrecision.NS)]

# Write all these points at once. I suggest collecting in batches.
write_api.write(bucket,org,pts)

# Flush data
write_api.close()

# Query to see if data was actually written
query = 'from(bucket:"TEST") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
print("Data creation display")
for table in tables:
    print(table)
    for row in table.records:
        print(row.values)

# Delete all data
del_client.delete('1970-01-01T00:00:00Z','2021-04-27T00:00:00Z','_measurement=point1',bucket=bucket,org=org)
#del_client.delete('1970-01-01T00:00:00Z','2021-04-27T00:00:00Z','_measurement=point2',bucket=bucket,org=org)
#del_client.delete('1970-01-01T00:00:00Z','2021-04-27T00:00:00Z','_measurement=point3',bucket=bucket,org=org)

# Query again to verify deletion
query = 'from(bucket:"TEST") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
print("Data deletion display")
for table in tables:
    print(table)
    for row in table.records:
        print(row.values)
client.close()

