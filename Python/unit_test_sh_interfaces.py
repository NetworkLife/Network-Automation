#!/usr/bin/python
# Open a file with a "show interfaces" and extract all interesting informations
# version: 0.1

'''
Create the following table from a "show interfaces"
+--------+-----------+-----------+-----------------------+-----------------------+-------------+----------+-----+--------+-------------+-------+--------+--------+------------------+-------------+---------+-----------+-----------+--------+------------+------------+----------------+
| SWITCH | SWITCH_IP | INTERFACE | PORT STATUS (up/down) | LINE STATUS (up/down) | DESCRIPTION | PORT MAC | MTU | DUPLEX | RELIABILITY |TXLOAD | RXLOAD | DUPLEX | AUTONEG (on/off) | Output drop | IN runt | In giants | IN errors | IN CRC | IN overrun | OUT errors | OUT collisions |
+--------+-----------+-----------+-----------------------+-----------------------+-------------+----------+-----+--------+-------------+-------+--------+--------+------------------+-------------+---------+-----------+-----------+--------+------------+------------+----------------+
'''

# REGEX
import re

# NAPALM
from napalm import get_network_driver

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

hand = open('show_interface.txt')
for line in hand:
    row = []   
    line = line.rstrip()
	
	#SWITCH & IP
    row.append(switch)
    row.append(switch_ip)
		

'''
Print the table
'''
for line in twod_list:
    print(line)
