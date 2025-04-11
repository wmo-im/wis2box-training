# fake-global-broker-and-cache

To run a local MQTT broker and a local cache that can be used to simulate the global broker and cache in the WIS2 environment during WIS2 training sessions.

# Usage

Update the file ``hostnames.txt`` with the hostnames or IPs of the student VMs.

Start the containers with the following command:

```bash
docker-compose -f docker-compose.yml up -d
```
This will start the following containers:
* `mosquitto` - local MQTT broker
* `minio` - local cache
* `republisher` - republisher that subscribes to the local MQTT broker and republishes messages to the global cache

To check the status of the connections to the local MQTT brokers defined in ``hostnames.txt``, run the following command:

```bash
docker logs -f republisher
```

# Environment variables

Environment values are defined `wis2-gb-gc.csv`, no need to update these when using the local training hardware

