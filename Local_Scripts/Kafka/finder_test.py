#!/usr/bin/python3
import re, sys
node_name=sys.argv[1]
filename="Output_Files/epc.log"
log = open(filename,"rt")
match_dict = dict()# Dictionary of matches
ue_rx = []      # List of UE REGEX
enb_rx = []     # List of eNB REGEx
epc_rx = []     # List of EPC REGEX
ues = set()     # Set of active UEs
results = []    # List of SMAC-customized dictionaries

#UE Filters
ue_rx.append(re.compile(r'''
               (?P<key>(type|clock_rate|EARFCN|f_dl|f_ul|Mode|PCI|PRB|CFO|c-rnti))[=]
               (?P<value>-?[.\d\w]+)''', re.VERBOSE))
ue_rx.append(re.compile(r'''
               (?P<key>IP)[:\s]+
               (?P<value>[.\d]+)''', re.VERBOSE))
#eNB Filters
enb_rx.append(re.compile(r'''
                    (?P<key>type|clock_rate|DL|UL)[=]
                    (?P<value>[.\d\w]+)''', re.VERBOSE))
#EPC Filters
epc_rx.append(re.compile(r'''
                    (?P<key>MCC|MNC|Name|id|PLMN|TAC|S1-U Address)[:]\s+
                    (?P<value>[.\d\w]+)''', re.VERBOSE))
epc_rx.append(re.compile(r'''
                    (?P<key>IMSI)[:]\s+
                    (?P<value>[\d]{15})''', re.VERBOSE))
epc_rx.append(re.compile(r'''
                    (?P<key>^Detach)[^\d]+
                    (?P<value>\d+)''', re.VERBOSE))
epc_rx.append(re.compile(r'''
                    (?P<key>^Deleting eNB)[^\d]+
                    (?P<value>[\d\w]+)''', re.VERBOSE))
# Scan through file
for line in log:
    if "ue" in filename:
        for re in ue_rx:
            for m in re.finditer(line):
                match_dict[node_name+"_"+m.group('key')]=m.group('value')
    elif "enb" in filename:
        for re in enb_rx:
            for m in re.finditer(line):
                match_dict[node_name+"_"+m.group('key')]=m.group('value')
        if "connected" in line:
            x=line.split()
            ues.add(x[1])
        if "Disconnecting" in line:
            s=line.split('=')
            ue_id=s[1].strip(".\n")
            if ue_id in ues:
                ues.remove(ue_id)
    elif "epc" in filename:
        for re in epc_rx:
            for m in re.finditer(line):
                if m.group('key') == "IMSI":
                    ues.add(m.group('value'))
                elif m.group('key') == "Detach":
                    ues.remove(m.group('value'))
                else:
                    match_dict[node_name+"_"+m.group('key')]=m.group('value')
print(match_dict)
