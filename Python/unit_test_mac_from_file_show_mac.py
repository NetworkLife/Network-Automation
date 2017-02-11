#!/usr/bin/python
# Open a file with a "show mac address-table" and extract VLAN, MAC address, Port
# version: 0.1

'''
Create the following table from a "show mac address-table"
+--------+-----------+------+-----+------+-------------------------------------+--------------------+
| SWITCH | SWITCH_IP | VLAN | MAC | PORT | Type of Mac (if known) : AP, IMP... | Good vlan ? (BOOL) |
+--------+-----------+------+-----+------+-------------------------------------+--------------------+
'''

# Declare variables
AP_CISCO_MAC = "00fe"
AP_CISCO_VLAN = 895

PRINTER_MAC = "00ce"
PRINTER_VLAN = 200

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

	#VERIFY if the mac address is a known type
    if (mac[:4] == AP_CISCO_MAC):
        row.append("AP_CISCO")
    elif (mac[:4] == PRINTER_MAC):
        row.append("PRINTER")
    else:
        row.append("")

	#VERIFY if the mac address match the good vlan
    if (mac[:4] == AP_CISCO_MAC) and (vlan[0] != AP_CISCO_VLAN):
        row.append(False)
    elif (mac[:4] == AP_CISCO_MAC) and (vlan[0] == AP_CISCO_VLAN)
        row.append(True)
    elif (mac[:4] == PRINTER_MAC) and (vlan[0] != PRINTER_VLAN):
        row.append(False)
    elif (mac[:4] == PRINTER_MAC) and (vlan[0] == PRINTER_VLAN)
        row.append(True)
    else:
        row.append("")

    twod_list.append(row)

'''
Print the table
'''
for line in twod_list:
    print(line)

'''
Generate the config for the wrongly configured ports
+--------+-----------+------+-----+------+-------------------------------------+--------------------+
| SWITCH | SWITCH_IP | VLAN | MAC | PORT | Type of Mac (if known) : AP, IMP... | Good vlan ? (BOOL) |
+--------+-----------+------+-----+------+-------------------------------------+--------------------+

 if MAC is AP and VLAN is NOK, then reconfigure
 if MAC is PRINTER and VLAN is NOK, then reconfigure

'''

for line in twod_list:
    print(line)