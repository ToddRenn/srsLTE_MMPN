#!/usr/bin/python3
import time
import threading
import reader

topic = "ue1_csv"
log = open("Output_Files/ue_metrics.csv","r")
#line="20;-48;48;-6762.984863;3.4;29;0.50;4562.417969;0;2.6;7.6;0.0;45223.968750;43;0.0;0.0;0.0;1.0"
for line in log:
    reader.csv_reader(line,topic)

