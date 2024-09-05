# Environment variables

* ``MINIO_HOST`` - MINIO host and port used to act as the fake global cache, e.g. ``instructor.wis2.training:9000`` 
* ``MINIO_KEY``  - MINIO access key / user ID for writing to the fake cache, e.g. ``wis2box``
* ``MINIO_SECRET`` - MINIO secret for writing to the fake cache 
* ``GC_URL`` - Base URL used to access files on the fake cache, e.g.  ``http://instructor.wis2.training``
* ``GB_HOST`` - Host name of the MQTT broker to republish to, e.g. ``instructor.wis2.training``
* ``GB_UID`` - User ID used for publishing, e.g. ``wis2box``
* ``GB_PWD`` - Password used for publishing

# Usage

In the VM run:

``python subscribe_and_republish.py``