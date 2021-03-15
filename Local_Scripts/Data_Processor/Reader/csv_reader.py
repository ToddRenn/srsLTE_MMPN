#!/bin/python3
from influx_reader import init_influx_dict as init
from influx_reader import update_actives as update
from influx_reader import write, query_api, bucket, org
from datetime import datetime

def csv_reader(csv_in,location,NODE_ID):
    # This function reads in a CSV string, matches it with expected headers,
    # and creates a custom dictionary which represents the JSON SMAC command
    # csv_in: The CSV input (string)
	# location: Node location (string)
    # NODE_ID: The node id (string)

	# Initialize UE if not present
    #if not NODE_ID in ues:
        #init(NODE_ID,location,ues)

    influx_data=init(NODE_ID,location)

	# Set the CSV headers
    header=['time','rsrp','pl','cfo','dl_mcs','dl_snr','dl_turbo','dl_brate','dl_bler',\
            'ul_ta','ul_mcs','ul_buff','ul_brate','ul_bler','rf_o','rf_u','rf_l','is_attached']

	# Split the string based on delimiter value
    s = csv_in.split(";")
    s[len(s)-1]=s[len(s)-1].strip('\n') # Get rid of the newline from last

    # If we're reading the CSV header, don't proceed
    if s[0]=='time':
        return

    # Create key/value pairs - skip the first column: time
    for i in range(1,len(header)):
        if header[i] == 'is_attached':
            if s[i] == '1.0':
                influx_data['fields'][header[i]] = 'Yes'
            else:
                influx_data['fields'][header[i]] = 'No'
        else:
            influx_data['fields'][header[i]] = float(s[i])

	# Update the timestamp
    time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    influx_data['time']=time

	# Write to InfluxDB
    write.write(bucket,org,influx_data)
    write.close()	# This flu sh may  or may not be efficient... consider batches
