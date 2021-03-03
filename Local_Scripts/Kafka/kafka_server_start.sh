#!/bin/bash

read -p "POWDER Username: " uName
read -p "PC#: " pcNum

addr="${uName}@pc${pcNum}.emulab.net"

gnome-terminal --tab -- bash -ic "ssh -p22 ${addr}; exec bash"
gnome-terminal --tab -- bash -ic "ssh -p22 ${addr}; exec bash"
gnome-terminal --tab -- bash -ic "ssh -p22 ${addr}; exec bash"
