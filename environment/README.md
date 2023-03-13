# Training environment

The wis2box portable training environment consists of the following components:
- One (1) Nighthawk WiFi router
- Three (3) ZOTAX ZBOX Mini PCs (M Series Edge MI623)

Each ZOTAX ZBOX Mini PC has been fitted with:
- 64 GB Memory
- 2 TB SSD

The ZOTAX ZBOX Mini PCs are running virtualization software: ProxMox version 7.3.

The 3 PCs together are setup in a ProxMox cluster to provide VMs for participants during the training.

The Nighthawk is setup to broadcast a password-protected WiFi network with SSID **WIS2-training**.
The local network is defined by 10.0.0.1/22

Adminstrators can access training environment from the following locations:

- Nighthawk WiFi router interface at https://10.0.0.1
- ProxMox cluster interface at https://10.0.1.1:8006

Each VM host has a 'vm-clone-base'-template from which new VMs can be created.

The 'vm-clone-base' template consists of:

- 2 vCPUs
- 48 GB local storage
- 4 GB RAM
- Ubuntu 20.0.4 with the following tools installed
    - Docker CE
    - mosquitto-clients
    - python3
    - python3-pip
    - unzip
    - docker-compose
    - minio pywis-pubsub (installed via `pip3`)
- `/etc/docker/daemon.json` with a Docker registry mirror pointing to http://10.0.2.222:5000

### VM naming convention

ProxMox hosts running on mini PCs:

- vm-host-1: 10.0.1.1
- vm-host-2: 10.0.2.1
- vm-host-3: 10.0.3.1

Student VMs:

- on vm-host-1: 10.0.1.11, 10.0.1.12, 10.0.1.13 etc.
- on vm-host-2: 10.0.2.11, 10.0.2.12, 10.0.2.13 etc.
- on vm-host-2: 10.0.3.11, 10.0.3.12, 10.0.3.13 etc.

local-repo-vm: 10.0.2.222

### MinIO setup

MinIO is used to provide the exercise materials and documentation.  The `local-repo-vm-222` VM must be started in
order to create MinIO storage.  The following buckets must be created manually with `readonly` permissions:

- `exercise-materials`
- `documentation`
