#!/usr/bin/python
# Multi-Backup script to TFTP
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

# VARs
tftp = "10.17.1.72";

def print_output(results):
    
    print ("\nSuccessful devices:");
    for a_dict in results:
        for identifier,v in a_dict.items():		
            (success, out_string) = v
            if success:
                #print ('#' * 20);
                print ('Device = {0}, {1}\n'.format(identifier,out_string));
                #print ('#' * 20);

    print ("\n\nFailed devices:\n");
    for a_dict in results:
        for identifier,v in a_dict.items():
            (success, out_string) = v
            if not success:
                print ('Device failed = {0}, {1}\n'.format(identifier,out_string));

    print ("\nEnd time: " + str(datetime.now()));
    print

def backup_configs(a_device, mp_queue):
    '''
	Copying Config to TFTP Server
    Return a dictionary where the key is the device identifier
    Value is (success|fail(boolean), return_string, name_of_device)
    '''    

    identifier = '{ip}'.format(**a_device)
    return_data = {}
#   backup_to_tftp_result = []

    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])
	
    try:
        net_connect = SSHClass(**a_device)
        hostname = net_connect.find_prompt()
        tftp_command = 'copy running-config tftp://{0}/{1}-{2}-config'.format(tftp,hostname[:-1],a_device['ip']);
        backup_to_tftp_result = net_connect.send_command_timing(tftp_command)
        if '[' in backup_to_tftp_result:
            backup_to_tftp_result += net_connect.send_command_timing("\n")
        if '[' in backup_to_tftp_result:
            backup_to_tftp_result += net_connect.send_command_timing("\n")
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return_data[identifier] = (False, e)
    
	# Add data to the queue (for parent process)
    mp_queue.put(return_data)
    return None

    return_data[identifier] = (True, backup_to_tftp_result)
    mp_queue.put(return_data)
	
def main():

    mp_queue = multiprocessing.Queue()
    processes = []

    print ("\nStart time: " + str(datetime.now()));

    for a_device in all_devices:
	
        p = multiprocessing.Process(target=backup_configs, args=(a_device, mp_queue))
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