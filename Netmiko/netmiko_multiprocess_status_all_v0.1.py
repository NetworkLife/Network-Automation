#!/usr/bin/python
# Report some status from show commands 
# version: 0.1

# Catch Paramiko warnings about libgmp and RandomPool
import warnings
with warnings.catch_warnings(record=True) as w:
    import paramiko

import multiprocessing
from datetime import datetime

import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

# DEVICE_CREDS contains the devices to connect to
from DEVICE_CREDS import all_devices

def print_output(results):
    
    print ("\nSuccessful devices:");
    for a_dict in results:
        for identifier,v in a_dict.items():
            (success, out_string) = v
            if success:
                print (out_string);

    print ("\n\nFailed devices:\n");
    for a_dict in results:
        for identifier,v in a_dict.items():
            (success, out_string) = v
            if not success:
                print ('Device failed = {0}'.format(identifier));

    print ("\nEnd time: " + str(datetime.now()));
    print

def worker_show_version(a_device, mp_queue):
    '''
    Return a dictionary where the key is the device identifier
    Value is (success|fail(boolean), return_string)
    '''    

    try:
        a_device['port']
    except KeyError:
        a_device['port'] = 22

    identifier = '{ip}'.format(**a_device)
    return_data = {}
    output = ""

    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])

    try:
        net_connect = SSHClass(**a_device)
        # Hostname
        hostname = net_connect.find_prompt()
        hostname = hostname[:-1]
        output += ">>>>> {0}: {1}\n".format(hostname,a_device['ip'])
        
        # Uptime
        uptime = net_connect.send_command("sh ver | inc uptime")
        output += "------- Uptime ---------\n"
        output += uptime
        output += "\n------------------------\n"
        
        # IOS Version
        show_ver_ios = net_connect.send_command("sh ver | inc System image file is")
        show_ver_ios_stripped = show_ver_ios.replace("System image file is ", "")
        show_ver_ios_stripped = show_ver_ios_stripped.replace("\"", "")
        output += "------- IOS Ver --------\n"
        output += show_ver_ios_stripped
        output += "\n------------------------\n"
        
        # PS Status
        show_env_ps = net_connect.send_command("sh env | inc PS1 |PS2 ")
        output += "------- PS Status ------\n"
        output += show_env_ps
        output += "\n------------------------\n"
        
        # Any environment Alarm ?
        show_env_alarm = net_connect.send_command("sh env alarm")
        output += "------- Env alarm ------\n"
        output += show_env_alarm
        output += "\n------------------------\n"
        output += "\n\n"
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return_data[identifier] = (False, e)

        # Add data to the queue (for parent process)
        mp_queue.put(return_data)
        return None

    return_data[identifier] = (True, output)
    mp_queue.put(return_data)
	
def main():

    mp_queue = multiprocessing.Queue()
    processes = []

    print ("\nStart time: " + str(datetime.now()));

    for a_device in all_devices:
        p = multiprocessing.Process(target=worker_show_version, args=(a_device, mp_queue))
        processes.append(p)
        # start the work process
        p.start()	
	
    # wait until the child processes have completed
    for p in processes:
        p.join()
		
    # retrieve all the data from the queue
    results = []
    for p in processes:
        results.append(mp_queue.get())
		
    print_output(results)

    
if __name__ == '__main__':

    main()