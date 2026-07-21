# Revue de sécurité — scripts Network Automation (2017)

Date de la revue : 2026-07-21
Périmètre : l'intégralité du dépôt (premier commit : 2017-02-08), soit les scripts Netmiko / Python / TextFSM d'automatisation de commutateurs Cisco (labo/tutoriel personnel, cf. `readme.md`).

## Résumé

Ce sont des scripts d'apprentissage (basés en partie sur le cours Netmiko de Kirk Byers — hôtes `csr1`, `pyclass`, `ntc`), pas du code de production, mais ils sont publiés sur un dépôt public et contiennent des pratiques qui seraient dangereuses si réutilisées telles quelles sur une vraie infrastructure. Le problème le plus important est la présence d'identifiants en clair, committés depuis la création du dépôt.

| # | Sévérité | Constat |
|---|----------|---------|
| 1 | **Élevée** | Identifiants en clair committés dans Git (répétés dans 4 fichiers `DEVICE_CREDS.py` + `Netmiko/netmiko.py`) |
| 2 | **Élevée** | Sauvegarde de configuration via TFTP (non chiffré, non authentifié) |
| 3 | Moyenne | Vérification de la clé d'hôte SSH non maîtrisée (comportement par défaut Paramiko/Netmiko) |
| 4 | Moyenne | Python 2 obsolète (EOL janvier 2020) dans plusieurs scripts |
| 5 | Faible | Fichiers de sortie écrits sans contrôle des permissions (CSV/backups contenant IP, MAC, n° de série) |
| 6 | Faible | Gestion d'exceptions trop large et peu de journalisation |
| 7 | Info | Aucune injection de commande shell identifiée (les scripts ne passent pas d'entrée utilisateur à `os.system`/`subprocess`) |

## Détail des constats

### 1. Identifiants en clair committés (Élevée)

Fichiers concernés :
- `Netmiko/DEVICE_CREDS.py`
- `backup-multiple-switches-to-tftp/DEVICE_CREDS.py`
- `interfaces-infos-from-multiple-switches-to-csv/DEVICE_CREDS.py`
- `inventory-infos-from-multiple-switches-to-csv/DEVICE_CREDS.py`
- `Netmiko/netmiko.py` (plusieurs jeux d'identifiants en dur : `ntc`/`ntc123`, `pyclass`/`password`, `admin`/`password`/`secret`)

Exemple (`DEVICE_CREDS.py`, identique dans les 4 copies) :
```python
DEVICE_1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.40.128',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
    'port': 22,
}
```

Risques :
- Ces identifiants sont dans l'historique Git depuis 2017 : les supprimer aujourd'hui ne les efface pas des anciens commits, accessibles à quiconque clone le dépôt.
- Le triplet `cisco`/`cisco`/`cisco` (utilisateur/mot de passe/secret enable) est un identifiant par défaut classique de labo — s'il a un jour été réutilisé sur un équipement réel, il doit être considéré comme compromis et changé.
- Le motif « credentials en dur dans un fichier Python importé » est le genre de code qu'on copie-colle ensuite dans un vrai script de production sans y penser.

Recommandations :
- Retirer les secrets du code : variables d'environnement, `getpass.getpass()` pour une saisie interactive, ou un coffre-fort (Ansible Vault, HashiCorp Vault, fichier `.env` ajouté au `.gitignore`).
- Ajouter un `.gitignore` pour tout fichier de creds futur, et envisager de purger l'historique (`git filter-repo` / BFG) si ces identifiants ont un jour servi sur du matériel réel — sinon, un simple commit de nettoyage suffit puisqu'il s'agit de creds de labo.

### 2. Sauvegarde de configuration via TFTP (Élevée)

`backup-multiple-switches-to-tftp/netmiko_multiprocess_backup_all.py` exécute `copy running-config tftp://...` sur chaque équipement.

TFTP (UDP/69) n'a ni authentification ni chiffrement. La configuration complète part en clair sur le réseau — elle peut contenir des community strings SNMP, des hash de mots de passe, des clés pré-partagées (VPN, routage), des ACL — et atterrit sur le serveur TFTP sans contrôle d'accès.

Recommandation : utiliser SCP/SFTP (Netmiko propose un transfert de fichiers via SCP) ou, à défaut, restreindre strictement le flux TFTP à un VLAN de management isolé et non routé.

### 3. Vérification de la clé d'hôte SSH (Moyenne)

Aucun des scripts ne configure explicitement la politique d'acceptation des clés d'hôte SSH (paramètres Netmiko/Paramiko tels que la gestion de `known_hosts`). Le comportement par défaut peut accepter silencieusement une clé hôte inconnue, ce qui ouvre la voie à une interception (MITM) si un attaquant est positionné sur le chemin réseau entre le script et l'équipement.

Recommandation : pour un usage au-delà du labo, épingler ou vérifier explicitement les clés hôtes des équipements.

### 4. Python 2 obsolète (Moyenne)

`Netmiko/netmiko.py` et `Netmiko/netmiko_multiprocess.py` sont écrits en Python 2 (`print output;`, `raw_input`, `dict.iteritems()`), une version en fin de vie depuis janvier 2020, qui ne reçoit plus aucun correctif de sécurité. Le reste du dépôt a déjà été migré en Python 3.

Recommandation : migrer les deux fichiers restants, et s'assurer que `netmiko`/`paramiko` sont à jour (plusieurs CVE historiques sur paramiko, ex. gestion des clés/algorithmes).

### 5. Fichiers de sortie sans contrôle des permissions (Faible)

`show_interfaces.txt`, `outfile.csv`, les fichiers de sauvegarde, etc. sont créés avec les permissions par défaut du process (souvent world-readable) et contiennent des données d'inventaire réseau (IP, MAC, description de ports, numéros de série). Sur une machine multi-utilisateurs, ces fichiers sont lisibles par tout le monde.

Recommandation : restreindre les permissions (`os.chmod(..., 0o600)`) sur les fichiers de sortie sensibles.

### 6. Gestion d'exceptions large et peu de journalisation (Faible)

Les blocs `except (NetMikoTimeoutException, NetMikoAuthenticationException)` avalent l'erreur sans journalisation exploitable. En cas d'échec d'authentification répété (ex. verrouillage de compte ou tentative détectée côté équipement), rien n'est tracé de façon à alerter un opérateur.

### 7. Pas d'injection de commande shell identifiée (Info, point positif)

Aucun script ne construit de commande shell locale (`os.system`, `subprocess`) à partir d'une entrée utilisateur ou d'une sortie d'équipement. Le seul assemblage de commande dynamique (`tftp_command` dans le script de backup) est envoyé à l'équipement réseau lui-même via Netmiko, pas à un shell local — risque très faible.

## Conclusion

Rien ici n'indique une compromission active, et le code est explicitement présenté comme un labo d'apprentissage. Le point à corriger en priorité si ce dépôt continue à vivre est la suppression des identifiants en dur (constat n°1), suivie du remplacement du TFTP par SCP/SFTP pour les sauvegardes de configuration (constat n°2).

## Correctifs appliqués

Les changements suivants ont été apportés dans cette même branche (PR #1) pour traiter les constats actionnables :

| Constat | Correctif |
|---------|-----------|
| 1 — Identifiants en dur | Les 4 `DEVICE_CREDS.py` lisent désormais les identifiants depuis les variables d'environnement (`NET_USERNAME` / `NET_PASSWORD` / `NET_SECRET`), avec repli sur une saisie interactive via `getpass`. Plus aucun mot de passe en clair dans le code. `Netmiko/netmiko.py` est annoté pour préciser que ses identifiants sont des valeurs d'exemple de tutoriel. |
| 2 — Backup TFTP | Le script de sauvegarde récupère la `running-config` via la session SSH déjà chiffrée et l'écrit localement (répertoire `backups/`), au lieu de `copy running-config tftp://...`. Fichiers créés en `0600`. Le bug de flux (`return None` avant la mise en queue du succès) est corrigé au passage. |
| 4 — Python 2 | `netmiko.py`, `netmiko_multiprocess.py` et `mac_converter.py` migrés en Python 3 (`print()`, `input()`, `dict.items()`), indentation de boucle corrigée. |
| 5 — Permissions | Les fichiers `outfile.csv` et les sauvegardes de config sont créés avec des droits restreints (`chmod 0600`). |
| 6 — Journalisation | Le script de backup utilise le module `logging` pour tracer les échecs au lieu de les avaler silencieusement. |
| — | Ajout d'un `.gitignore` couvrant secrets (`.env`, `credentials.py`), sauvegardes de config et sorties générées. |

Constats laissés en l'état (choix documenté) :
- **n°3 (clé d'hôte SSH)** : nécessite une infrastructure `known_hosts` propre à l'environnement de déploiement ; non pertinent à figer dans des scripts de labo. Recommandation maintenue pour un usage en production.
- Le répertoire `backup-multiple-switches-to-tftp/` conserve son nom d'origine (référencé dans le `readme.md` et l'historique) bien que le TFTP ait été retiré.
- Les fichiers d'exemple déjà committés (`TextFSM/outfile.csv`, etc.) sont conservés comme jeux de données de démonstration ; le `.gitignore` empêche seulement les futurs.
