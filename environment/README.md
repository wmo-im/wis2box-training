# Training environment

The training environment requires one student VM per participant, matching the [wis2box system requirements](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#system-requirements).

The VMs can be provided by:
- the portable training environment
- the local organizer providing VMs on their own infrastructure
- VMs provided using the European Weather Cloud (EWC) infrastructure

The current default is for the WMO Secretariat to use VMs in the European Weather Cloud.

## setting up the environment in the European Weather Cloud

The European Weather Cloud (EWC) can be used to provide student VMs during local training sessions.

The scripts used by WMO Secretariat to setup the EWC environment can be found in the directory `EWC-VM-setup-scripts`, they are based on using openstack CLI commands to create VMs in the EWC. The DNS entries for the VMs are created in the `training.wis2dev.io` domain that is managed by the WMO Secretariat.

The scripts create VMs using the a naming convention based on the username provided as input to the script:
- VM name: `<username>-training-wis2dev-io`
- FQDN: `<username>.training.wis2dev.io`

The script will setup a new user with the username provided and autogenerate a password for the user. The latest wis2box-release is downloaded and unzipped in the home directory of the new user along with the exercise materials.

Note that the European Weather Cloud does not allow ports for Grafana (3000) and MinIO (9000) to be exposed publicly. Therefore the student will need to use an SSH tunnel to access these services from the student VM.


