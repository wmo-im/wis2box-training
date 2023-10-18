# Instructor helpers

This directory contains resources that may be valuable for instructors as part of
delivery of the training.  Note that the below need to be run while connected to
the **WIS2-training** Wi-Fi network.

# Local global services

Local global services provide a test environment to simulate WIS2 workflows using
the classroom as a network of WIS2 nodes.

## Global Broker

TBD

### Live map (`live.html`)

Serve this webpage via HTTP on your VM.  Ensure that the following line:

```javascript
const host = 'ws://tbd.wis2.training:8884/ws';
```

...is updated to point to the Global Broker installed above.

## Global Cache

[wis2-gc](https://github.com/wmo-im/wis2-gc) is a Reference Implememtation of
a WIS2 Global Cache (GC).  Follow the setup instructions, pointing
to the Global Broker installed above.

## Global Discovery Catalogue

[wis2-gdc](https://github.com/wmo-im/wis2-gdc) is a Reference Implememtation of
a WIS2 Global Discovery Catalogue (GDC).  Follow the setup instructions, pointing
to the Global Broker installed above.

# Other

* `instructor_bashrc.sh`: sample bash prompt to help with screen readability while
  displaying a termnial during a practical session.
