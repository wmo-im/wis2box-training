# fake-global-broker-and-cache

To run a local MQTT broker and a local cache that can be used to simulate the global broker and cache in the WIS2 environment during WIS2 training sessions.

# NOTE

If you want to use a wis2box-instance to serve the purpose of the fake global cache and fake global broker, the following changes are required on the services included by the wis2box-stack:

* Update acf.conf in the "mosquitto" container to allow the wis2box-user to publish on `cache/a/wis2/#` (restart the container after making changes)
* create the bucket "cache" in the "wis2box-minio" container and set the access policy to public

# Environment variables

Environment values are defined `wis2-gb-gc.csv`, no need to update these when using the local training HW

* ``MINIO_HOST`` - MINIO host and port used to act as the fake global cache, e.g. ``global-cache.wis2.training:9000`` 
* ``MINIO_KEY``  - MINIO access key / user ID for writing to the fake cache, e.g. ``wis2training``
* ``MINIO_SECRET`` - MINIO secret for writing to the fake cache, corresponds to WIS2BOX_STORAGE_PASSWORD
* ``GC_URL`` - Base URL used to access files on the fake cache, e.g.  ``http://global-cache.wis2.training:9000``
* ``GB_HOST`` - Host name of the MQTT broker to republish to, e.g. ``global-cache.wis2.training``
* ``GB_UID`` - User ID used for publishing, e.g. ``wis2training``
* ``GB_PWD`` - Password used for publishing, e.g ``wis2training``

# Usage

Update the file ``wis2nodes.json`` with the hostnames or IPs of the student VMs.

In the VM run:

``python subscribe_and_republish.py``

Run this scripts *after* all students ran the `python3 wis2box-ctl.py start` command to start the wis2box stack.
