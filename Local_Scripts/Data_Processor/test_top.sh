#!/bin/bash
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue1_csv 155.98.36.82 moran 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue1_log 155.98.36.82 moran 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py enb1_log 155.98.36.82 moran 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py epc1_log 155.98.36.82 moran 2; exec bash"

sleep 2

gnome-terminal --tab -- bash -ic "python3 producer.py ue1_csv ue_metrics.csv; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py ue1_log ue.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py enb1_log enb.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py epc1_log epc.log; exec bash"
