#!/usr/bin/python
# TUTORIAL / BASICs examples of Netmiko library 
# version: 0.1

from netmiko import ConnectHandler
from datetime import datetime
#import os
#import subprocess
#import sys

# ------------------------------------ #
# ------ Connection SSH - Method 1 --- #
# ------------------------------------ #

platform = 'cisco_ios'
host = 'csr1'
username = 'ntc'
password = 'ntc123'
device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)

# ------------------------------------ #
# ------ Connection SSH - Method 2 --- #
# ------------------------------------ #

cisco = {
'device_type': 'cisco_ios',
'ip': '10.10.10.227',
'username': 'pyclass',
'password': 'password'
} 

net_connect = ConnectHandler(**cisco)

# ------------------------------------ #
# ------ Connection SSH - Method 3 --- #
# ------------------------------------ #

net_connect = ConnectHandler(device_type='cisco_ios', ip='10.10.10.227', username='pyclass', password='password') 


# ------------------------------------ #
# ------ Connection SSH - Prompt ----- #
# ------------------------------------ #

net_connect.find_prompt()

# ------------------------------------ #
# ------ show command ---------------- #
# ------------------------------------ #

output = device.send_command('show version')
print output;

# -------------------------------------------- #
# ------ send config command - one by one ---- #
# -------------------------------------------- #

device.config_mode()
device.send_command('interface fast1/0')
device.send_command('ip addr 10.10.10.10 255.255.255.0')
device.exit_config_mode()

# --------------------------------------------- #
# ------ send config command - multiple ------- #
# --------------------------------------------- #

commands = ['interface fa1/0', 'no shut']
device.send_config_set(commands)

# --------------------------------------------- #
# ------ send command to multiple devices ----- #
# --------------------------------------------- #

# First, define the networking devices:


cisco_881 = {
'device_type': 'cisco_ios',
'ip':   '10.10.10.227',
'username': 'pyclass',
'password': 'password',
'verbose': False,
}
 
cisco_asa = {
'device_type': 'cisco_asa',
'ip': '10.10.10.10',
'username': 'admin',
'password': 'password',
'secret': 'secret',
'verbose': False,
}
  
# Next, I need to create a Python list that includes all of these devices:

all_devices = [cisco_881, cisco_asa] 

# 3. create a for loop that iterates over all of these devices. 
# Each time through the loop: the code will connect to the device, execute the 'show arp' command, and then display the output. 
# I will also keep track of the time that it takes for the code execute.

start_time = datetime.now()
for a_device in all_devices:
net_connect = ConnectHandler(**a_device)
output = net_connect.send_command("show arp")
print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(a_device['device_type'])
print output
print ">>>>>>>>> End <<<<<<<<<"
 
end_time = datetime.now()

total_time = end_time - start_time 

#Here is the output from the for loop (i.e. all of the "show arp" output):

#>>>>>>>>> Device cisco_ios <<<<<<<<<
#Protocol  Address          Age (min)  Hardware Addr   Type   Interface
#Internet  10.220.88.1             4   001f.9e92.16fb  ARPA   FastEthernet4
#Internet  10.220.88.20            -   c89c.1dea.0eb6  ARPA   FastEthernet4
#Internet  10.220.88.100          10   f0ad.4e01.d933  ARPA   FastEthernet4
#>>>>>>>>> End <<<<<<<<<

#>>>>>>>>> Device cisco_asa <<<<<<<<<
#    inside 10.220.88.100 f0ad.4e01.d933 251
#    inside 10.220.88.31 5254.0001.3737 311
#    inside 10.220.88.39 6464.9be8.08c8 361
#    inside 10.220.88.30 5254.0092.13bb 1451
#    inside 10.220.88.10 0018.fe1e.b020 1700
#>>>>>>>>> End <<<<<<<<<

#>>> print total_time
#0:00:44.791650

#As you can see it took almost 45 seconds for the above for-loop to execute. This could be significantly improved by executing the SSH sessions in parallel, for an example of this see the code here

# ------------------------------------ #
# ------ closing SSH session --------- #
# ------------------------------------ #

device.disconnect()

# ----------------------- #
# --- Netmiko methods --- #
# ----------------------- #
#net_connect.config_mode() -- Enter into config mode
#net_connect.check_config_mode() -- Check if you are in config mode, return a boolean
#net_connect.exit_config_mode() -- Exit config mode
#net_connect.clear_buffer() -- Clear the output buffer on the remote device
#net_connect.enable() -- Enter enable mode
#net_connect.exit_enable_mode() -- Exit enable mode
#net_connect.find_prompt() -- Return the current router prompt
#net_connect.commit(arguments) -- Execute a commit action on Juniper and IOS-XR
#net_connect.disconnect() -- Close the SSH connection
#net_connect.send_command(arguments) -- Send command down the SSH channel, return output back
#net_connect.send_config_set(arguments) -- Send a set of configuration commands to remote device
#net_connect.send_config_from_file(arguments) -- Send a set of configuration commands loaded from a file
