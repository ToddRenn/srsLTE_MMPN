#!/usr/bin/python3

# This script takes file(s) as arguments, extracts info from the data
# and interfaces with SMAC accordingly.

import sys
import scipy
import requests

data = {
            "hostname": "localhost",
            "portnum": 9091,
            "system": "true",
            "version": "2.4",
            "units": "None",
            "type": "String",
			"forceEnable": "true",
            "sensor": "",
            "value": "",
            "command": "update-sensor",
            "timeout": 5
            }

def update_sensor(data):
    url = 'http://localhost:9091'
    json_file = open("file.json","w")
    json_file.write(str(data)+"SYSTEMMONITOR_COMMANDER_TRANSMISSION_COMPLETE")
    json_file.close()
    payload = open("file.json")
    r=requests.post(url, data=payload)


def log_reader(name):
	output=scipy.fromfile(open(name), dtype=scipy.float32)
	location="/home/mwinters/Documents/MMPN/Matt_C2I_C/C2I/utilities/smac-commander/Node_Data/"+name
	filename=name
	with open(location,"w") as results:
		for line in output:
			results.write(str(line))
	data["value"]=location
	data["sensor"]="Location of "+name+" data"
	update_sensor(data)

if __name__ == '__main__':
    # loop through all arguments - excluding script call (argv[0])
    for arg in sys.argv[1:]:
        if "csv" in arg:
            csv_reader(arg)
        else:
            log_reader(arg)


