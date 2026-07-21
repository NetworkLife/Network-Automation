#!/usr/bin/env python3
# Multi-Backup script des configurations
# version: 0.2
#
# Changement de securite (cf. SECURITY_REVIEW.md, constat n2) :
# la sauvegarde ne passe plus par TFTP (protocole non chiffre et non
# authentifie). La running-config est recuperee directement via la session
# SSH deja chiffree, puis ecrite localement avec des droits restreints (0600).

import logging
import multiprocessing
import os
import stat
from datetime import datetime

# Catch Paramiko warnings about libgmp and RandomPool
import warnings
with warnings.catch_warnings(record=True):
    import paramiko  # noqa: F401

import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

# DEVICE_CREDS contains the devices to connect to
from DEVICE_CREDS import all_devices

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Repertoire de destination des sauvegardes
BACKUP_DIR = os.environ.get('BACKUP_DIR', 'backups')


def print_output(results):

    print("\nSuccessful devices:")
    for a_dict in results:
        for identifier, v in a_dict.items():
            (success, out_string) = v
            if success:
                print('Device = {0}, {1}'.format(identifier, out_string))

    print("\n\nFailed devices:\n")
    for a_dict in results:
        for identifier, v in a_dict.items():
            (success, out_string) = v
            if not success:
                print('Device failed = {0}, {1}'.format(identifier, out_string))

    print("\nEnd time: " + str(datetime.now()))


def backup_configs(a_device, mp_queue):
    '''
    Recupere la running-config via SSH et l'ecrit dans un fichier local (0600).
    Retourne un dictionnaire {identifier: (success(bool), message)}.
    '''

    identifier = '{ip}'.format(**a_device)
    return_data = {}

    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])

    try:
        net_connect = SSHClass(**a_device)
        hostname = net_connect.find_prompt()[:-1]
        running_config = net_connect.send_command('show running-config')
        net_connect.disconnect()

        os.makedirs(BACKUP_DIR, exist_ok=True)
        filename = '{0}-{1}-config.txt'.format(hostname, a_device['ip'])
        path = os.path.join(BACKUP_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(running_config)
        # Restreindre les droits : la config peut contenir des secrets
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600

        return_data[identifier] = (True, 'saved to {0}'.format(path))
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        logger.warning('Backup failed for %s: %s', identifier, e)
        return_data[identifier] = (False, str(e))

    mp_queue.put(return_data)


def main():

    mp_queue = multiprocessing.Queue()
    processes = []

    print("\nStart time: " + str(datetime.now()))

    for a_device in all_devices:
        p = multiprocessing.Process(target=backup_configs, args=(a_device, mp_queue))
        processes.append(p)
        p.start()

    # wait until the child processes have completed
    for p in processes:
        p.join()

    # retrieve all the data from the queue
    results = []
    for _ in processes:
        results.append(mp_queue.get())

    print_output(results)


if __name__ == '__main__':
    main()
