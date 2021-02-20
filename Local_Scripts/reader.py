#!/usr/bin/python3

# This script takes file(s) as arguments, extracts info from the data
# and interfaces with SMAC accordingly.

import csv
import os
import subprocess
import sys
import time

def tail(thefile):
    thefile.seek(0,2) # Look at last line of thefile

    while not thefile.closed:   # Continue running until file is closed
        line = thefile.readline()
        if not line:            # If no new line is written, wait
            time.sleep(5)
            continue
        if line and line.endswith('\n') # If line is written AND it's complete
            yield line

def update_sensor(name,value):
    args=['./utilities/smac-commander/smac-commander', 'update-sensor', \
        '--system', '--sensor='+name, '--type=Double', '--units=Celcius', \
        '--min-val=0', '--max-val=100', '--value='+value, 'force-enable=true']

    subprocess.run(args)

def csv_reader(file):
    metrics = csv.DictReader(tail(open(file,"rt")), delimeter=';')
    for row in metrics:
        for key in row.keys():
            update_sensor(key, row.get(key))

def log_reader(file):
    #fill this

if __name__ == '__main__':
    # loop through all arguments - excluding script call (argv[0])
    for arg in sys.argv[1:]:
        if "csv" in arg:
            csv_reader(arg)
        else:
            log_reader(arg)
