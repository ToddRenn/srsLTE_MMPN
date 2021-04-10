#!/bin/bash
KAF_IP=155.98.39.10

# Run consumers
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue1_csv ${KAF_IP} moran 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue1_log ${KAF_IP} moran 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py enb1_log ${KAF_IP} MEB 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue2_csv ${KAF_IP} bookstore 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py ue2_log ${KAF_IP} bookstore 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py enb2_log ${KAF_IP} browning 2; exec bash"
gnome-terminal --tab -- bash -ic "python3 Reader/consumer.py epc1_log ${KAF_IP} browning 2; exec bash"

sleep 2

# Run producers
gnome-terminal --tab -- bash -ic "python3 producer.py ue1_csv ue_metrics.csv; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py ue1_log ue1.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py ue2_csv ue_metrics.csv; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py ue2_log ue2.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py enb1_log enb1.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py enb2_log enb2.log; exec bash"
gnome-terminal --tab -- bash -ic "python3 producer.py epc1_log epc.log; exec bash"
