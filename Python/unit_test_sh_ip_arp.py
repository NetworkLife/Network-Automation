#!/usr/bin/python
# Open a file with a "show ip arp" and extract IP address, MAC address, Vlan
# version: 0.1

'''
Create the following table from a "show ip arp"
+--------+-----------+----+-----+------+
| SWITCH | SWITCH_IP | IP | MAC | VLAN |
+--------+-----------+----+-----+------+
'''

import re

'''
function to remove the [' at the beginning and and '] at the end of a string
'''
def remove_re_format(input):
    output = str(input)
    output = output[2:len(output)]
    output = output[0:(len(output)-2)]
    return output


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
        row.append(remove_re_format(ip))
    else:
        row.append("")	
    #MAC
    if re.search(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line):
        mac = re.findall(r'[0-9a-fA-F]{4}[.][0-9a-fA-F]{4}[.][0-9a-fA-F]{4}', line)
        row.append(remove_re_format(mac))
    else:
        row.append("")
		
	#VLAN
    if re.search(r'[V][l][a][n]\d{1,3}', line):
        vlan = re.findall(r'[V][l][a][n]\d{1,3}', line)
        vlan = remove_re_format(vlan)
        row.append(vlan[4:len(vlan)])
    else:
        row.append("")

    twod_list.append(row)

for line in twod_list:
    print(line)