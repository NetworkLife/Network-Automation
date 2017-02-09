#!/usr/bin/python
# version: 0.1

import netmiko
import time

# DEVICE_CREDS contains the devices to connect to
from DEVICE_CREDS import all_devices

for a_device in all_devices:
    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])
    net_connect = SSHClass(**a_device)
    tftp = "10.17.1.72";
    hostname = net_connect.find_prompt()
    tftp_command = 'copy running-config tftp://{0}/{1}-{2}-config'.format(tftp,hostname[:-1],a_device['ip']);
    print (tftp_command)
    output = net_connect.send_command_timing(tftp_command)
    if '[' in output:
        output += net_connect.send_command_timing("\n")
    if '[' in output:
        output += net_connect.send_command_timing("\n")
    print (output)
