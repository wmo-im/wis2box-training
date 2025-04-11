from datetime import datetime as dt
import json
import logging
from minio import Minio
import os.path
from pathlib import Path
import paho.mqtt.client as mqtt
from paho.mqtt import publish as pub
import tempfile
import threading
import urllib3
import uuid
import time

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

tictoc = 0
nworkers = 4

# MinIO storage for saving data to
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET = os.getenv('MINIO_ROOT_PASSWORD')
# Fake global cache url
GC_URL = os.getenv('GC_URL')
# Fake global broker
GB_HOST = os.getenv('WIS2BOX_BROKER_HOST')
GB_UID = os.getenv('WIS2BOX_BROKER_USERNAME')
GB_PWD = os.getenv('WIS2BOX_BROKER_PASSWORD')

print(f"MINIO_HOST={MINIO_HOST}")
print(f"MINIO_KEY={MINIO_KEY}")
print(f"GC_URL={GC_URL}")
print(f"GB_HOST={GB_HOST}")
print(f"GB_UID={GB_UID}")

def on_connect(client, userdata, flags, rc):
    client.subscribe("origin/a/wis2/#")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    # if topic contains metadata or data, republish on original topic, else do nothing
    if 'metadata' in msg.topic:
        print("Republishing metadata")
    elif 'data' in msg.topic:
        print("Republishing data")
    else:
        print(f"Not republishing data with topic {msg.topic}")
        return
    # republish using the origin topic on this broker
    pub.single(
            topic = msg.topic,
            payload = json.dumps(payload),
            hostname = GB_HOST,
            auth={"username": GB_UID, "password": GB_PWD}
        )
    print(f"Republished to {msg.topic}")
    # if topic contains data/core or metadata, download to cache
    if 'data/core' in msg.topic:
        print("Downloading core data")
    elif 'metadata' in msg.topic:
        print("Downloading metadata")
    else:
        print(f"Not downloading data with topic {msg.topic}")
        return
    # download and save to data dir
    canonical = None
    canonical_idx = None
    idx = 0
    for link in payload.get("links"):
        if link.get("rel") is not None:
            if link.get("rel") == "canonical":
                canonical = link.get("href")
                canonical_idx = idx
                break
        idx += 1

    data_id = Path(payload.get("properties").get("data_id"))
    p = f"{data_id.parent}"
    # remove origin
    p = p.replace("origin/", "")
    filename = f"{data_id.name}"

    if canonical is not None:
        # download data
        print("Downloading")
        http = urllib3.PoolManager()
        response = http.request("GET", canonical)
        # save to tempory file
        temp = tempfile.NamedTemporaryFile(mode="w")
        with open(temp.name, "wb") as fh:
            fh.write(response.data)
        # connect to MinIO
        try:
            minio_client = Minio(MINIO_HOST, access_key=MINIO_KEY,
                           secret_key=MINIO_SECRET, secure=False)
        except Exception as e:
            LOGGER.error("Error connecting to Minio")
            raise e

        try:
            minio_client.fput_object("cache", f"{p}/{filename}", temp.name)
        except Exception as e:
            print(f"Error putting object in cache: {e}")
            raise e

        # update data id and href
        try:
            payload["properties"]["data_id"] = f"cache/{p}/{filename}"
            payload["links"][canonical_idx]["href"] = \
                f"{GC_URL}/cache/{p}/{filename}"
            payload["id"] = str(uuid.uuid4())
            payload["properties"]["pubtime"] = dt.now().isoformat()
            topic = msg.topic.replace("origin","cache")
        except Exception as e:
            print(e)
            raise e

        pub.single(
            topic = topic,
            payload = json.dumps(payload),
            hostname = GB_HOST,
            auth={"username": GB_UID, "password": GB_PWD}
        )
        print(f"Published to {topic}")


def subscribe(**kwargs):
    try:
        client = kwargs.get('client')
        broker = kwargs.get('broker')
        host = broker.get("host")
        port = broker.get("port")
        uid = broker.get("uid")
        pwd = broker.get("pwd")
    except Exception as e:
        raise e
    client.username_pw_set(uid, pwd)
    client.on_connect = on_connect
    client.on_message = on_message
    while True:  # Retry loop
        try:
            client.connect(host=host, port=port)
            print(f"Connected to host={host}")
            with open(f"{host}.log", "w") as fh:
                fh.write("connected")
            client.loop_forever()
        except Exception as e:
            # msg = f"Failed to connect to host={host}, retrying in 5 seconds..."
            # LOGGER.error(msg)
            # LOGGER.error(e)
            # remove the file if it exists
            if os.path.exists(f"{host}.log"):
                os.remove(f"{host}.log")
            time.sleep(5)  # Wait before retrying


def main():
    # connect to MinIO
    try:
        minio_client = Minio(MINIO_HOST, access_key=MINIO_KEY,
                           secret_key=MINIO_SECRET, secure=False)
    except Exception as e:
        print("Error connecting to Minio")
        raise e

    print("Minio connected")

    if minio_client.bucket_exists("cache"):
        print("Bucket cache exists")
    else:
        print("Bucket cache does not exist, creating")
        
        try:
            minio_client.make_bucket("cache")
        except Exception as e:
            print("Error creating bucket")
            raise e

    # Set bucket policy to allow public read access
    policy_readonly = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::cache/*"]
            }
        ]
    }
    try:
        minio_client.set_bucket_policy("cache", json.dumps(policy_readonly))
        print("Public read policy set for bucket 'cache'")
    except Exception as e:
        print("Error setting bucket policy")
        raise e

    # Load configurations
    idx = 0
    # create the brokers list from the hostnames.txt
    brokers = []
    with open("/app/hostnames.txt") as f:
        for line in f:
            # remove new line
            line = line.strip()
            if len(line) > 0:
                brokers.append({
                    "host": line,
                    "port": 1883,
                    "uid": "everyone",
                    "pwd": "everyone",
                    "protocol": "tcp"
                })

        # set up clients
        clients = []
        idx = 0
        for broker in brokers:
            clients.append( mqtt.Client(transport=broker.get('protocol')))
            idx += 1
        conn_threads = []
        idx = 0
        for broker in brokers:
            conn_threads.append(
                threading.Thread(target=subscribe, kwargs={"client": clients[idx], "broker": broker}, daemon=True) # noqa
            )
            idx += 1

        for t in conn_threads:
            t.start()

        with open("sub.lock", "w") as fh:
            fh.write("Running")

        running = True
        while running:
            # print the hosts connected by reading the log files
            nconn = 0
            for broker in brokers:
                try:
                    with open(f"{broker.get('host')}.log", "r") as fh:
                        print(f"Host {broker.get('host')} connected")
                        nconn += 1
                except Exception as e:
                    print(f"Host {broker.get('host')} not connected")
            print("****")
            print(f"**** {nconn} OUT OF {len(brokers)} WIS2 NODES CONNECTED")
            print("****")
            # sleep for 15 seconds
            time.sleep(15)
            if os.path.exists("sub.lock"):
                continue
            else:
                running = False

        for client in clients:
            client.disconnect()


        for t in conn_threads:
            if t is not None:
                t.join()

if __name__ == '__main__':
    main()