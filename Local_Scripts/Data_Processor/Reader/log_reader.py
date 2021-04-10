#!/bin/python3
from influx_reader import init_influx_dict as init
from influx_reader import update_actives as update
from influx_reader import query_info, bucket
from datetime import datetime
import re

epc_new_enb=False
epc_new_ue=False
ue_new=False
enb_new=False

ue_init={}
enb_init={}
enb_temp={}
ue_temp={}

active_ue=[]
def log_reader(log,location,NODE_ID):
    global epc_new_ue, epc_new_enb, enb_new, ue_new     # Data recording triggers
    global enb_temp, ue_temp, enb_init, ue_init         # Temp storage vars
    global active_enb, active_ue, active_ues            # Active lists
    ue_rx = []                                          # List of UE REGEX
    enb_rx = []                                         # List of eNB REGEX
    epc_rx = []                                         # List of EPC REGEX

    # Filters
    # ue_rx[0] - Basic UE info
    ue_rx.append(re.compile(r'''
                            (?P<key>(type|clock_rate|EARFCN|f_dl|f_ul|Mode|PCI|PRB|c-rnti))[=]
                            (?P<value>-?[.\d\w]+)''', re.VERBOSE))
    # ue_rx[1] - IP info
    ue_rx.append(re.compile(r'''
                            (?P<key>IP)[:\s]+
                            (?P<value>[.\d]+)''', re.VERBOSE))
    # Basic eNB tags
    enb_rx.append(re.compile(r'''
                             (?P<key>type|clock_rate|DL|UL)[=]
                             (?P<value>[.\d\w]+)''', re.VERBOSE))
    # epc_rx[0] - eNB info
    epc_rx.append(re.compile(r'''
                             (?P<key>MCC|MNC|Name|id|PLMN)[:]\s?
                             (?P<value>[\d\w]+)''', re.VERBOSE))
    # epc_rx[1] - UE IP info
    epc_rx.append(re.compile(r'''
                             (?P<key>IP|IMSI)\s
                             (?P<value>[.\d]+)''', re.VERBOSE))
    # epc_rx[2] - Release UE info
    epc_rx.append(re.compile(r'''
                             (?P<key>^Detach)[^\d]+
                             (?P<value>\d+)''', re.VERBOSE))
    # epc_rx[3] - Release eNB info
    epc_rx.append(re.compile(r'''
                             (?P<key>^Deleting eNB)[^\d]+
                             (?P<value>[\d\w]+)''', re.VERBOSE))

    # Create tags from log file values
    if "ue" in NODE_ID:
        # Initialize UE if not already present
        #if not NODE_ID in ues:
            #init(NODE_ID,location,ues)

        # Get setup info for this UE
        if "Opening USRP" in log:
            print("New UE detected: "+NODE_ID)
            ue_new=True
        if "Random Access Transmission" in log:
            print("Finished setting up UE")
            print(str(ue_init))
            ue_new=False
            update(ue_init,location,'Add',NODE_ID)
            ue_init.clear()
            return
        if ue_new:
            for m in ue_rx[0].finditer(log):
                print("Key: "+str(m.group('key'))+"\tValue: \
                      "+str(m.group('value')))
                ue_init[m.group('key')]=m.group('value')
            return
        # c-rnti
        if "Random Access Complete" in log:
            ue_init['Name']=NODE_ID
            for m in ue_rx[0].finditer(log):
                print("Key: "+str(m.group('key'))+"\tValue: \
                      "+str(m.group('value')))
                ue_init[m.group('key')]=m.group('value')
            update(ue_init,location,'Add',NODE_ID)
            #ue_init.clear()
            return

        # Get IMSI from EPC entry
        for m in ue_rx[1].finditer(log):
            print("Key: "+str(m.group('key'))+"\tValue: \
                      "+str(m.group('value')))
            ue_init[m.group('key')]=m.group('value')

            #if m.group('key') == 'IP':
                #ue_init['IMSI']=
                #auth_info=next(x for x in active_ue if x['IP']==m.group('value'))
                #ue_init = {**ue_init,**auth_info}
            update(ue_init.copy(),location,'Add',NODE_ID)

    elif "enb" in NODE_ID:
        # New eNB initializing, start trigger
        if "Opening USRP" in log:
            print("New eNB detected")
            enb_new=True

        if "eNodeB started" in log:
            print("Adding "+NODE_ID+" from "+location+".")
            print(str(enb_init))
            enb_new=False
            update(enb_init,location,'Add',NODE_ID)
            enb_init.clear()
            return

        if enb_new:
            # Find REGEX matches
            for rx in enb_rx:
                for m in rx.finditer(log):
                    enb_init[m.group('key')]=m.group('value')
            return

    elif "epc" in NODE_ID:
        # EPC log does two things:
        # 1. Report on new eNB/UE connections + identifiers
        # 2. Report on eNB/UE disconnections

        # Start "recording" when a eNB connects
        if "Received S1" in log:
            print("New eNB detected")
            epc_new_enb = True
            return

        # Update active eNBs after new eNB setup finishes
        if "Sending S1" in log:
            epc_new_enb = False
            update(enb_temp.copy(),location,'Add',enb_temp.copy().get('Name'))
            enb_temp.clear()
            return

        if epc_new_enb:
            # Get eNB info
            print("Retrieving eNB information")
            for m in epc_rx[0].finditer(log):
                #print("Key: "+str(m.group('key'))+"\tValue: "+str(m.group('value')))
                enb_temp[m.group('key')]=m.group('value')
            return

        # Start "recording" when a UE connects
        if "SPGW Allocated IP" in log:
            print("New UE detected")
            for m in epc_rx[1].finditer(log):
                ue_temp[m.group('key')]=m.group('value')

        # Add new UE data to Active UEs
        if "Adding attach" in log:
            print("Adding UE: "+str(ue_temp['IMSI'])+ \
                  "\tUE IP: "+str(ue_temp['IP']))
            epc_new_ue = False
            update(ue_temp.copy(),location,'Add',ue_temp.copy().get('IP'))
            ue_temp.clear()

        if "Deleting eNB" in log:
            s=log.split(" ")
            enb_id=s[5].strip("\n")
            print("Removing eNB: "+enb_id)
            enb_to_remove=query_info(bucket, 'id', enb_id)
            r_str="".join(enb_to_remove)
            print(r_str)
            update(None,location,'Delete',r_str)

        if "Detach request --" in log:
            s=log.split(" ")
            ue_imsi=s[4].strip("\n")
            print("Removing UE: "+ue_imsi)
            ue_ip=query_info(bucket, 'IMSI', ue_imsi)
            r_str="".join(ue_ip)
            ue_to_remove=query_info(bucket,'IP',r_str)
            print(ue_to_remove)
            for ue in ue_to_remove:
                ue_str="".join(ue)
                print("Removing measurement: "+ue_str)
                update(None,location,'Delete',ue_str)
