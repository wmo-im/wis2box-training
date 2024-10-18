# fake-global-broker-and-cache

To run a local MQTT broker and a local cache that can be used to simulate the global broker and cache in the WIS2 environment during WIS2 training sessions.

# NOTE

If you want to use a wis2box-instance to serve the purpose of the fake global cache and fake global broker, the following changes are required on the services included by the wis2box-stack:

* Update acf.conf in the "mosquitto" container to allow the wis2box-user to publish on `cache/a/wis2/#` (restart the container after making changes)
* create the bucket "cache" in the "wis2box-minio" container and set the access policy to public

# Environment variables

Define these in a local ``.env`` file or in the environment of the VM.

* ``MINIO_HOST`` - MINIO host and port used to act as the fake global cache, e.g. ``instructor.wis2.training:9000`` 
* ``MINIO_KEY``  - MINIO access key / user ID for writing to the fake cache, e.g. ``wis2box`` when using wis2box
* ``MINIO_SECRET`` - MINIO secret for writing to the fake cache, corresponds to WIS2BOX_STORAGE_PASSWORD when using wis2box
* ``GC_URL`` - Base URL used to access files on the fake cache, e.g.  ``http://instructor.wis2.training:9000``
* ``GB_HOST`` - Host name of the MQTT broker to republish to, e.g. ``instructor.wis2.training``
* ``GB_UID`` - User ID used for publishing, e.g. ``wis2box`` when using wis2box
* ``GB_PWD`` - Password used for publishing, corresponds to WIS2BOX_BRIDGE_PASSWORD when using wis2box

# Usage

Update the file ``wis2nodes.json`` with the hostnames or IPs of the student VMs.

In the VM run:

``python subscribe_and_republish.py``

Run this scripts *after* all students ran the `python3 wis2box-ctl.py start` command to start the wis2box stack.
