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
AP_CISCO_MAC = "00f2"
AP_CISCO_VLAN = 895
AP_CISCO_TEMPLATE = (" switchport access vlan {0}\n description ** AP **\n shut\n no shut".format(AP_CISCO_VLAN))

PRINTER_MAC = "0025"
PRINTER_VLAN = 200
PRINTER_TEMPLATE = (" switchport access vlan {0}\n description ** PRINTER **\n shut\n no shut".format(PRINTER_VLAN))

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
        row.append(remove_re_format(mac))
    else:
        row.append("")
        mac = ""

	#PORT
    if re.search(r'[P][o][r][t][-][c][h][a][n][n][e][l][\s\S]+', line):
        port = re.findall(r'[P][o][r][t][-][c][h][a][n][n][e][l][\s\S]+', line)
        row.append(remove_re_format(port))
    elif re.search(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line):
        port = re.findall(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line)
        row.append(remove_re_format(port))
    elif re.search(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line):
        port = re.findall(r'[G][i][g][a][b][i][t][E][t][h][e][r][n][e][t][\s\S]+', line)
        row.append(remove_re_format(port))
    else:
        row.append("")

	#VERIFY if the mac address is a known type
    mac4 = str(mac)
    mac4 = mac4[2:6]
    print ("\n")
    if mac4 == AP_CISCO_MAC:
        row.append("AP_CISCO")
    elif mac4 == PRINTER_MAC:
        row.append("PRINTER")
    else:
        row.append(mac4)

	#VERIFY if the mac address match the good vlan
    if mac4 == AP_CISCO_MAC and int(vlan[0]) != int(AP_CISCO_VLAN):
        row.append(False)
    elif mac4 == AP_CISCO_MAC and int(vlan[0]) == int(AP_CISCO_VLAN):
        row.append(True)
    elif mac4 == PRINTER_MAC and int(vlan[0]) != int(PRINTER_VLAN):
        row.append(False)
    elif (mac4 == PRINTER_MAC) and int(vlan[0]) == int(PRINTER_VLAN):
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

 if MAC is AP and VLAN is NOK, then reconfigure with the good template
 if MAC is PRINTER and VLAN is NOK, then reconfigure with the good template
'''

output_file = ""
switch = 'switch {0} {1}'.format(switch,switch_ip)
print (switch)
output_file += switch
output_file += "\n"

print ('*'*len(switch))
output_file += ('*'*len(switch))
output_file += "\n"

for line in twod_list:
    switch_name = line[0]
    switch_ip = line[1]
    vlan = line[2]
    mac = line[3]
    port = line[4]
    type = line[5]
    good = line[6]
	
    #if the vlan is wrongly configured and the port is not an uplink (Port-Channel)
    if not good and port[0:12] != "Port-channel":
	
	    #if it's an AP, configure it as an AP
        if type is "AP_CISCO":
            print('interface {0}'.format(port))
            output_file += ('interface {0}'.format(port))
            output_file += "\n"
            print('{0}\n'.format(AP_CISCO_TEMPLATE))
            output_file += ('{0}\n'.format(AP_CISCO_TEMPLATE))

	    #if it's a PRINTER, configure it as a PRINTER
        if type is "PRINTER":
            print('interface {0}'.format(port))
            output_file += ('interface {0}'.format(port))
            output_file += "\n"
            print('{0}\n'.format(PRINTER_TEMPLATE))
            output_file += ('{0}\n'.format(PRINTER_TEMPLATE))

'''
generate a config file
'''
file = open("new_config.txt","w") 
file.write(output_file) 
file.close() 