#!/bin/bash

c2i_filepath="~/Documents/MMPN_Repo/C2I/"

# Source Files
source ./func_wrapper.sh

# Step 0. Import EML files
import_eml_file

# Step 1. Launch Jupiter DB
tput setaf 6
echo "Starting Jupiter DB..."
tput sgr0
gnome-terminal --tab -- bash -ic "source ./func_wrapper.sh; start_jupiter_server; set_title 'Jupiter DB'; exec bash"

# Monitor the log file for Jupiter DB
(tail -f -n0 ${c2i_filepath}logs/jupiter-server.log &) | grep -q 'server is ready'
tput setaf 10
echo 'Jupiter server is ready.'

# Step 2. Start plugins
tput setaf 6
echo "Starting plugins..."
gnome-terminal --tab -- bash -ic "source ./func_wrapper.sh; start_plugins;set_title 'Plugins'; exec bash"
tput sgr0
sleep 2

# Step 3. Start C2I-C
tput setaf 6
echo "Starting C2I-C..."
gnome-terminal --tab -- bash -ic "source ./func_wrapper.sh; start_c2i; set_title 'C2I-C'; exec bash"
tput sgr0
sleep 2

# Step 4. Start SMAC-Commander
tput setaf 6
echo "Starting SMAC-Commander..."
gnome-terminal --tab -- bash -ic "source ./func_wrapper.sh; start_smac; set_title 'SMAC'; exec bash"
tput sgr0
