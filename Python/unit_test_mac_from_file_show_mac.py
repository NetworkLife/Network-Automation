#!/usr/bin/python
# Open a file with a "show mac address-table" and extract VLAN, MAC address, Port
# version: 0.1

import re

# Init two dimension list
twod_list = []
                              
switch = "SWITCH_NAME"
switch_ip = "SWITCH_IP"

hand = open('sh_mac.txt')
for line in hand:
    row = []   
    line = line.rstrip()
	
	#SWITCH & IP
    row.append(switch)
    row.append(switch_ip)
		
	#VLAN
    if re.search(r'\d{1,3}', line):
        vlan = re.findall(r'\d{1,3}', line)
        row.append(vlan[0])
    else:
        row.append("")	
    
	#MAC
    if re.search(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line):
        mac = re.findall(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line)
        row.append(mac)
    else:
        row.append("")

	#PORT
    if re.search(r'[P][o][r][t][-][c][h][a][n][n][e][l][\s\S]+', line):
        mac = re.findall(r'[P][o][r][t][-][c][h][a][n][n][e][l][\s\S]+', line)
        row.append(mac)
    elif re.search(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line):
        mac = re.findall(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line)
        row.append(mac)
    elif re.search(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line):
        mac = re.findall(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line)
        row.append(mac)
    else:
        row.append("")

    twod_list.append(row)

for line in twod_list:
    print(line)