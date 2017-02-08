#!/usr/bin/python
# Open a file with a "show ip arp" and extract IP address, MAC address, Vlan
# version: 0.1

import re

# Init two dimension list
twod_list = []
                              
switch = "SWITCH_NAME"
switch_ip = "SWITCH_IP"

hand = open('sh_ip_arp.txt')
for line in hand:
    row = []   
    line = line.rstrip()
	
	#SWITCH & IP
    row.append(switch)
    row.append(switch_ip)
	
    #IP
    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line):
        ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        row.append(ip)
    else:
        row.append("")	
    #MAC
    if re.search(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line):
        mac = re.findall(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line)
        row.append(mac)
    else:
        row.append("")
		
	#VLAN
    if re.search(r'[V][l][a][n]\d{1,3}', line):
        vlan = re.findall(r'[V][l][a][n]\d{1,3}', line)
        row.append(vlan)
    else:
        row.append("")

    twod_list.append(row)

for line in twod_list:
    print(line)