#!/usr/bin/env python3
# version: 0.2
# Sauvegarde de la running-config via SSH (plus de TFTP, cf. SECURITY_REVIEW.md).

import os
import stat

import netmiko

# DEVICE_CREDS contains the devices to connect to
from DEVICE_CREDS import all_devices

BACKUP_DIR = os.environ.get('BACKUP_DIR', 'backups')

for a_device in all_devices:
    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])
    net_connect = SSHClass(**a_device)
    hostname = net_connect.find_prompt()[:-1]
    running_config = net_connect.send_command('show running-config')
    net_connect.disconnect()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    path = os.path.join(BACKUP_DIR, '{0}-{1}-config.txt'.format(hostname, a_device['ip']))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(running_config)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600
    print('Saved {0}'.format(path))
