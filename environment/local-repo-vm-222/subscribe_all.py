import paho

connections=[
    {"broker":"127.0.0.1","port":2883},
    {"broker":"192.168.1.159","port":1883},
    {"broker":"192.168.1.65","port":1883},
]

import paho.mqtt.client as mqtt
mqtt.Client.connected_flag=False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        client.subscribe("origin/#")

def on_message(client, userdata, message):
    print("message received",str(message.payload.decode("utf-8")))

#create clients
for conn in connections:
   cname="Client"+str(conn['broker'])
   client=mqtt.Client(cname)
   client.on_connect = on_connect
   client.on_message = on_message
   conn["client"]=client

while 1!=0:
    for conn in connections:
        try :
            conn['client'].connect(conn['broker'],conn['port'])
            conn['client'].loop_start()
        except Exception as e:
            print(f"Failed to connect to {conn['broker']}")
            print(e)
            continue
        print(f"Connected to {conn['broker']}")