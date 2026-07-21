# Network Automation Scripts

A small collection of Python scripts to automate day-to-day tasks on Cisco
IOS / NX-OS switches: pulling operational data (`show` commands), parsing it
into CSV/tables with TextFSM, backing up configurations, and matching MAC
addresses to interfaces across a fleet of switches.

Originally written in 2017 as a learning project; reviewed and hardened in
2026 (see [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md)).

## Prerequisites

- **Python 3.6+** (the scripts have been migrated off Python 2)
- Network reachability (SSH/TCP 22) to the target devices
- A user account on each device with privileges for the `show` commands used

Python packages:

```bash
pip install netmiko paramiko textfsm
```

> `netmiko` pulls in `paramiko`; `textfsm` is only needed for the
> `interfaces-*` / `inventory-*` / `TextFSM` scripts.

## Credentials (important)

Credentials are **never** hardcoded. Each `DEVICE_CREDS.py` reads them from
environment variables, falling back to an interactive prompt if they are not
set:

| Variable | Purpose | Default |
|----------|---------|---------|
| `NET_USERNAME` | Login username | prompted |
| `NET_PASSWORD` | Login password | prompted (hidden) |
| `NET_SECRET`   | Enable secret  | falls back to `NET_PASSWORD` |
| `NET_DEVICE_IP`| Override the sample device IP | `192.168.40.128` |

```bash
export NET_USERNAME=myuser
export NET_PASSWORD='...'
export NET_SECRET='...'      # optional
```

Edit the `DEVICE_CREDS.py` in the relevant folder to list your own devices in
the `all_devices` list. Do **not** commit real credentials — a `.gitignore`
is provided that ignores `.env`, `credentials.py`, generated CSVs and config
backups.

## Usage

Run each script from inside its own directory (they expect their
`DEVICE_CREDS.py` and templates in the current folder):

```bash
cd interfaces-infos-from-multiple-switches-to-csv
python3 netmiko_multiprocess_ports_infos.py
```

## Contents

### `Netmiko/`
Basics and multiprocessing examples of the Netmiko library.
- **netmiko.py** — annotated tutorial of the connection / command methods (illustrative, example hosts).
- **netmiko_multiprocess.py** — run `show version` on many devices in parallel.
- **netmiko_multiprocess_status_all_v0.1.py** — report uptime, IOS version, PSU and environment alarms per device.

### `Python/`
Pure-Python parsing helpers (regex extraction of MAC / IP addresses, etc.).
- **unit_test_sh_ip_arp.py** — turn a `show ip arp` into a table.
- **unit_test_sh_mac.py** — turn a `show mac address-table` into a table.
- **concatenate_2_tables.py** — join the two tables above into a readable format.
- **mac_converter.py** — convert a MAC address between EUI, Cisco and Microsoft formats.

### `TextFSM/`
Examples using the TextFSM module with the ntc-templates collection.
- **templates/** — network-to-code TextFSM templates.
- **unit_test_sh_interfaces_to_csv.py** — parse a `show interfaces` into a CSV.
- **unit_test_sh_interfaces_to_table.py** — parse a `show interfaces` into a Python list.

### `backup-multiple-switches-over-ssh/`
Backup the running-config of multiple devices in parallel, **over the
encrypted SSH session** (no TFTP). Configs are written to a local `backups/`
directory with `0600` permissions. Set `BACKUP_DIR` to change the target
folder.

### `concatenate-show_ip_arp-and-show_mac_address/`
Concatenate a `show ip arp` and a `show mac address-table` to match MAC
addresses with the switch/interface where they are learned.

### `interfaces-infos-from-multiple-switches-to-csv/`
Extract `show interfaces` from all your switches and write them to
`outfile.csv` (created with `0600` permissions).

### `inventory-infos-from-multiple-switches-to-csv/`
Extract `show inventory` from all your switches and write them to
`outfile.csv` (created with `0600` permissions).

## Security

See [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md) for the full review and the
list of fixes applied (credentials handling, SSH-based backups, Python 3
migration, output-file permissions).

## Disclaimer

I'm not a dev — this is not fancy code, but it works (for me at least!). You
can seriously mess up your network with these scripts if you don't know what
you're doing. I take no responsibility for that. :)
