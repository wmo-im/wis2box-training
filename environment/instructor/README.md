# Instructor helpers

This directory contains resources that may be valuable for instructors as part of
delivery of the training. 

## terminal display when projecting

* `instructor_bashrc.sh`: sample bash prompt to help with screen readability while
  displaying a terminal during a practical session.

## Local global services

Local global services provide a test environment to simulate WIS2 workflows using the classroom as a network of WIS2 Nodes. 
See the `fake-global-broker-and-cache` and `fake-global-discovery-catalogue` directories.

During the training instructors can have:

- an MQTT Explorer session open to the local broker to demonstrate the flow of messages between the nodes
- a web browser open to the Global Discovery Catalogue to demonstrate the datasets cached in the local GDC

## Live map (`live.html`) (deprecated)

Serve this webpage via HTTP on your VM.  Ensure that the following line:

```javascript
const host = 'ws://tbd.wis2.training:8884/ws';
```

...is updated to point to the Global Broker installed above.
