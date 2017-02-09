#!/usr/bin/python 
# version: 0.1

import netmiko
import time

# DEVICE_CREDS contains the devices to connect to
from DEVICE_CREDS import all_devices

for a_device in all_devices:
    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])
    net_connect = SSHClass(**a_device)

    # Hostname
    hostname = net_connect.find_prompt()
    hostname = hostname[:-1]
    print (">>>>> {0}: {1}".format(hostname,a_device['ip']))

    # Uptime
    uptime = net_connect.send_command("sh ver | inc uptime")
    print ("------- Uptime ---------")
    print (uptime)
    print ("------------------------")

    # IOS Version
    show_ver_ios = net_connect.send_command("sh ver | inc System image file is")
    show_ver_ios_stripped = show_ver_ios.replace("System image file is ", "")
    show_ver_ios_stripped = show_ver_ios_stripped.replace("\"", "")
    print ("------- IOS Ver --------")
    print (show_ver_ios_stripped)
    print ("------------------------")

    # PS Status
    show_env_ps = net_connect.send_command("sh env | inc PS1 |PS2 ")
    print ("------- PS Status ------")
    print (show_env_ps)
    print ("------------------------")

    # Any environment Alarm ?
    show_env_alarm = net_connect.send_command("sh env alarm")
    print ("------- Env alarm ------")
    print (show_env_alarm)
    print ("------------------------")
    print ("\n\n")