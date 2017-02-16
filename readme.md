**Netmiko** 
 Contains tests of the Netmiko Library.

**Python** 
 Contains Python tests, Regex extractions of MAC, IP addresses...Etc.
- **unit_test_sh_ip_arp.py** - Take a "show ip arp" and transform in a table
- **unit_test_sh_mac.py** - Take a "show mac address-table" and transform in a table
- **concatenate_2_tables.py** - Take two previous tables and concatenate in readable format
- **mac_converter.py** - Convert mac address in EUI, Cisco, Microsoft format.

**textFSM** 
 Contains tests of the textFSM Python module
- **Templates** - Network2code templates for textFSM
- **unit_test_sh_interfaces_to_csv.py - convert "show interfaces" into an exploitable .csv
- **unit_test_sh_interfaces_to_table.py - convert "show interfaces" into an exploitable python list
  
**backup-multiple-switches-to-tftp**
- "copy run tftp" on multiple devices using Netmiko to backup all your devices in a few seconds.

**concatenate-show_ip_arp-and-show_mac_address**
- Concat "show ip arp" and "show mac address-table" to match MAC Addresses with interfaces of all switches.

**interfaces-infos-from-multiple-switches-to-csv**
- Extract "show interfaces" from all your switches and put them in an output.csv

**inventory-infos-from-multiple-switches-to-csv**
- Extract "show inventory" from all your switches and put them in an output.csv