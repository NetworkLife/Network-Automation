"""
Inventaire des équipements et identifiants de connexion.

Les identifiants ne sont PLUS stockés en clair dans le code (cf. constat n1 de
SECURITY_REVIEW.md). Ils sont lus depuis des variables d'environnement, avec un
repli sur une saisie interactive si elles ne sont pas definies :

    export NET_USERNAME=monuser
    export NET_PASSWORD=...
    export NET_SECRET=...          # secret "enable" (optionnel, defaut = password)
    export NET_DEVICE_IP=10.0.0.1  # optionnel, surcharge l'IP par defaut

Aucune valeur sensible ne doit etre commitee dans ce fichier.
"""

import os
from getpass import getpass

username = os.environ.get('NET_USERNAME') or input('Username: ')
password = os.environ.get('NET_PASSWORD') or getpass('Password: ')
secret = os.environ.get('NET_SECRET') or password

DEVICE_1 = {
    'device_type': 'cisco_ios',
    'ip': os.environ.get('NET_DEVICE_IP', '192.168.40.128'),
    'username': username,
    'password': password,
    'secret': secret,
    'port': 22,
    'verbose': False,
}

all_devices = [
    DEVICE_1,
]
