#!/usr/bin/python3
import re, sys
node_name=sys.argv[1]

ue = open("Output_Files/ue.log","rt")
ue_words=['Searching','Connected','PRB','rnti','Network']
matches=[]
match_dict=dict()
ue_rx = re.compile(r'''
                   (?P<key>\w[-_\w]+)[=]
                   (?P<value>-?[.\d\w]+)''', re.VERBOSE)
ue_ip = re.compile(r'''
                   (?P<key>IP)[:\s]+
                   (?P<value>[.\d]+)''', re.VERBOSE)
for line in ue:
    #if(any(word in line for word in ue_words)):
        matches.append([(m.group('key'), m.group('value')) for m in
                    ue_rx.finditer(line)])
        matches.append([(m.group('key'), m.group('value')) for m in
                    ue_ip.finditer(line)])
        for m in ue_ip.finditer(line):
            match_dict[node_name+"_"+m.group('key')]=m.group('value')
        for m in ue_rx.finditer(line):
            match_dict[node_name+"_"+m.group('key')]=m.group('value')

#results=list(filter(None,matches))
print(match_dict)
#for result in results:
    #print("Key: %s \t Value: %s"%(result[0],result[1]))

