#!/usr/bin/python

'''
Create the following table from a "show inventory" on multiple switches
+----------+------+-------------+------------+-----+---------------+
| HOSTNAME | NAME | DESCRIPTION | PRODUCT_ID | VID | SERIAL NUMBER |
+----------+------+-------------+------------+-----+---------------+
'''

import textfsm
import sys

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

def normalise_show_inventory_output(results):
    for a_dict in results:
        for identifier,v in iter(a_dict.items()):
            (success, out_string) = v
            if success:
                print ('{0}\n{1}'.format(identifier,out_string));
                print ('\n');
                print ('-'*40);
                print ('\n');		
    print	

def show_inventory(a_device, mp_queue):
    debug = True
    return_data = {}
	
    show_inventory_command = 'show inventory '
    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])

    try:
        net_connect = SSHClass(**a_device)
        hostname = net_connect.find_prompt()
        identifier = hostname
        identifier += '{ip}'.format(**a_device)
        show_inventory = net_connect.send_command_timing(show_inventory_command)
        return_data[identifier] = (True, show_inventory) 
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return_data[identifier] = (False, e)
        return None
       
    mp_queue.put(return_data)
		
def main():

    mp_queue = multiprocessing.Queue()
    processes = []
    print ("\nStart time: " + str(datetime.now()));

	# For each device, send a "show inventory"
    for a_device in all_devices:
        p = multiprocessing.Process(target=show_inventory, args=(a_device, mp_queue))
        processes.append(p)
        # start the work process
        p.start()	

    # wait until the child processes have completed
#    for p in processes:
#        p.join()
	
    # retrieve all the data from the "show inventory" queue
    results = []
    for p in processes:
        results.append(mp_queue.get())
	
	# add '-------------' between each "show interface" output
    #raw_text_data = normalise_show_inventory_output(results)
     	
    orig_stdout = sys.stdout
    fichier = open("show_inventory.txt", "w", encoding='utf-8')
    sys.stdout = fichier
    fichier.write(str(normalise_show_inventory_output(results)))
    sys.stdout = orig_stdout
    fichier.close()
	
	# Load the input file to a variable
    input_file = open("show_inventory.txt", encoding='utf-8')
    raw_text_data = input_file.read()
    input_file.close()
	
	# textFSM the output
    # The argument 'template' is a file handle and 'raw_text_data' is a 
    # string with the content from the previous show_inventory() function
    template = open("cisco_ios_show_inventory.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(raw_text_data)
 
    # the results are written to a CSV file
    outfile_name = open("outfile.csv", "w+")
    outfile = outfile_name
	 
	# Display result as CSV and write it to the output file
	# First the column headers...
    print(re_table.header)
    for s in re_table.header:
        outfile.write("%s;" % s)
    outfile.write("\n")
	 
    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)	

    print ("\nEnd time: " + str(datetime.now()));
    
if __name__ == '__main__':
    main()