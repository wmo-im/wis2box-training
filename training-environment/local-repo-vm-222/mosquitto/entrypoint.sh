#!/bin/sh

touch /mosquitto/config/password.txt
echo "Setting mosquitto authentication"
mosquitto_passwd -b -c /mosquitto/config/password.txt wmo_admin $MQTT_WMO_ADMIN_PASSWORD
mosquitto_passwd -b /mosquitto/config/password.txt everyone everyone

/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf