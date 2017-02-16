- **DEVICE_CREDS.py** contains the switches informations (Netmiko)
- **cisco_ios_show_interfaces.template** is the textFSM template

The Python script netmiko_multiprocess_ports_infos.py is :
- sending "show interfaces" on multiple switches with Netmiko multiprocessing (fast)
- storing the outputs and separating them with '----' between switches
- extracting the interesting interfaces informations with textFSM
- storing the textFSM output into an output.csv file