# Training environment

The training environment requires one student VM per participant, matching the [wis2box system requirements](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#system-requirements).

The VMs can be provided either by the portable training environment or by the local organizer providing VMs on their own infrastructure.

## Portable training environment

The wis2box portable training environment consists of the following components:
- One (1) Nighthawk Wi-Fi router
- Three (3) ZOTAX ZBOX Mini PCs (M Series Edge MI623)

Each ZOTAX ZBOX Mini PC has been fitted with:
- 64 GB Memory
- 2 TB SSD

The ZOTAX ZBOX Mini PCs are running virtualization software: ProxMox version 7.3.

The 3 PCs together are setup in a ProxMox cluster to provide VMs for participants during the training.

The Nighthawk is setup to broadcast a password-protected Wi-Fi network with SSID **WIS2-training**.
The local network is defined by 10.0.0.1/22

Administrators can access training environment from the following locations:

- Nighthawk Wi-Fi router interface at https://10.0.0.1
- ProxMox cluster interface at https://10.0.1.1:8006

Each VM host has a 'vm-clone-base' template from which new VMs can be created.

The 'vm-clone-base' template consists of:

- 2 vCPUs
- 48 GB local storage
- 4 GB RAM
- Ubuntu 22.0.4 LTS with the following system packages installed:
    - Docker CE v2.21.0
    - docker compose 24.0.6
    - packages installed via `pip3`:
      - minio
      - pywiscat

### VM naming convention

ProxMox hosts running on mini PCs:

- vm-host-1: 10.0.1.1
- vm-host-2: 10.0.2.1
- vm-host-3: 10.0.3.1

Student VMs:

- on vm-host-1: 10.0.1.11, 10.0.1.12, 10.0.1.13 etc.
- on vm-host-2: 10.0.2.11, 10.0.2.12, 10.0.2.13 etc.
- on vm-host-2: 10.0.3.11, 10.0.3.12, 10.0.3.13 etc.

The WiFi router has pre-configured mac-to-IP settings. After cloning the base template set the MAC address to match the IP using the following logic:

- `00:00:00:00:01:11` -> `10.0.1.11`
- `00:00:00:00:02:12` -> `10.0.2.12`
- etc.

### student VM setup

Student VMs can be setup by cloning the a base template.

The script `setup_student_vm.sh` can be used to by the `wmo_admin` account to create a new user account on the student VM and add the latest wis2box release to the home directory of the new user along with the exercise materials.

The script requires a username and an host-ip as input:

```bash
source setup_student_vm.sh mlimper 10.0.1.11
```

The DNS server needs to be **manually** configured for each training to map host-IPs to hostnames, e.g.: 10.0.1.11 -> `mlimper.wis2.training`

### local DNS

A local DNS server is setup on a VM with IP 10.0.2.111. 

DNS server UI
http://dns-server.wis2.training:5380/
or
http://10.0.2.111:5380/

The DNS server UI can be used to check the status of the DNS-server and/or to add additional A-records. 

**The DNS server needs to be manually pre-configured before each training with A-records naming each host for each local training participants.** 

The DNS server is hosted on a VM on vm-host-2. If vm-host-2 is lost during transit or broken a backup is available on vm-host-1. If the DNS-server for some reason does not work at all, participants can just use the IP as hostname.
