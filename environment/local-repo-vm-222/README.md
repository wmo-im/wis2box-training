# local-repo-vm-222

This is the stack to be run on the VM with IP 10.0.2.222

This stack is used to make a local set of services available within the **WIS2-training** network:

- docker-registry-mirror: to cache Docker images and reduce build time
- MinIO bucket: to make training materials locally available over HTTP
- mosquitto broker: to demonstrate MQTT and/or to act as potential local GB

A local `.env` is required to provide MinIO with a username and password for the `root` user and to set the password for the `wmo_admin` user on mosquitto.

```bash
MQTT_WMO_ADMIN_PASSWORD=XXX

MINIO_ROOT_USER=wmo_admin
MINIO_ROOT_PASSWORD=XXX
```
