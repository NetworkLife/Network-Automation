#!/usr/bin/python
# Concatenate "show ip arp" from a core switch and "show mac address-table" from all access switches
# version: 0.1

'''
Create the following table from a "show ip arp" and a "show mac address-table"
+-----------------++-----------------------------------------+
| from sh ip arp  || from sh mac address-table               |
+----+-----+------++--------+-----------+------+------+------+
| IP | MAC | VLAN || SWITCH | SWITCH_IP | PORT | TYPE | GOOD |
+----+-----+------++--------+-----------+------+------+------+
'''

#INITIALIZATION
table_show_ip_arp = [['SWITCH_NAME', 'SWITCH_IP', '', '', ''],
['SWITCH_NAME', 'SWITCH_IP', '10.84.12.10', '00f2.8b34.b6ac', '895'],
['SWITCH_NAME', 'SWITCH_IP', '10.84.12.11', '00f2.8b34.b8e0', '895'],
['SWITCH_NAME', 'SWITCH_IP', '10.84.12.12', '00f2.8b34.b8e1', '895'],
['SWITCH_NAME', 'SWITCH_IP', '10.84.12.13', '00f2.8b34.b8e2', '895'],
['SWITCH_NAME', 'SWITCH_IP', '10.84.12.14', '00f2.8b34.b8e3', '895']]

table_show_mac_add = [['SWITCH_NAME', 'SWITCH_IP', '', '', '', '', ''],
['SWITCH_NAME', 'SWITCH_IP', '50', '0025.00f0.95df', 'Port-channel1', 'PRINTER', False],
['SWITCH_NAME', 'SWITCH_IP', '50', '0025.00f0.97c5', 'GigabitEthernet5/44', 'PRINTER', False],
['SWITCH_NAME', 'SWITCH_IP', '200', '00f2.8b34.abd0', 'GigabitEthernet5/45', 'AP_CISCO', False],
['SWITCH_NAME', 'SWITCH_IP', '895', '00f2.8b34.b6ac', 'GigabitEthernet5/46', 'AP_CISCO', True],
['SWITCH_NAME', 'SWITCH_IP', '895', '00f2.8b34.b8e0', 'GigabitEthernet5/47', 'AP_CISCO', True],
['SWITCH_NAME', 'SWITCH_IP', '895', '00f2.8b34.b8e1', 'GigabitEthernet5/48', 'AP_CISCO', True],
['SWITCH_NAME', 'SWITCH_IP', '895', '00f2.8b34.b8e2', 'GigabitEthernet6/1', 'AP_CISCO', True],
['SWITCH_NAME', 'SWITCH_IP', '300', '00f2.8b34.b8e3', 'GigabitEthernet6/10', 'AP_CISCO', False],
['SWITCH_NAME', 'SWITCH_IP', '200', '0025.00f0.97c5', 'GigabitEthernet6/41', 'PRINTER', True],
['SWITCH_NAME', 'SWITCH_IP', '200', '0025.00f0.97c5', 'GigabitEthernet6/43', 'PRINTER', True],
['SWITCH_NAME', 'SWITCH_IP', '50', '0025.00f0.97c5', 'GigabitEthernet6/44', 'PRINTER', False],
['SWITCH_NAME', 'SWITCH_IP', '50', '0025.00f0.97c5', 'GigabitEthernet6/45', 'PRINTER', False]]

# Init two dimension list
twod_list = []

for line in table_show_ip_arp:
    row = []   
		
    ip = line[2]
    ip_mac = line[3]
    ip_vlan = line[4]
	
	#IP & MAC & VLAN
    row.append(ip)
    row.append(ip_mac)
    row.append(ip_vlan)

    for line2 in table_show_mac_add:
        switch_name = line2[0]
        switch_ip = line2[1]
        vlan = line2[2]
        mac = line2[3]
        port = line2[4]
        type = line2[5]
        good = line2[6]
	    
        if ip_mac == mac:
            row.append(switch_name)
            row.append(switch_ip)
            row.append(port)
            row.append(type)
            row.append(good)

    twod_list.append(row)

for line in twod_list:
    print(line)

'''
generate an output file
'''
file = open("concatenate_2_tables.txt","w") 
output_file = ""
for line in twod_list:
    output_file += str(line)
    output_file += "\n"
file.write(output_file)
file.close()