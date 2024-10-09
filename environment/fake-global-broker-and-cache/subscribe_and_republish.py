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

# use dotenv to load environment variables
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

tictoc = 0
nworkers = 4

# MinIO storage for saving data to
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_KEY = os.getenv('MINIO_KEY')
MINIO_SECRET = os.getenv('MINIO_SECRET')
# Fake global cache url
GC_URL = os.getenv('GC_URL')
# Fake global broker
GB_HOST = os.getenv('GB_HOST')
GB_UID = os.getenv('GB_UID')
GB_PWD = os.getenv('GB_PWD')

print(f"MINIO_HOST={MINIO_HOST}")
print(f"MINIO_KEY={MINIO_KEY}")
print(f"GC_URL={GC_URL}")
print(f"GB_HOST={GB_HOST}")
print(f"GB_UID={GB_UID}")

def on_connect(client, userdata, flags, rc):
    client.subscribe("origin/a/wis2/#")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(json.dumps(payload, indent=4))
    # if topic contains metadata or data, republish on original topic, else do nothing
    if 'metadata' in msg.topic:
        print("Republishing metadata")
    elif 'data' in msg.topic:
        print("Republishing data")
    else:
        print(f"Not republishing data with topic {msg.topic}")
        return
    # if topic contains data/core or metadata, download to cache
    if 'data/core' in msg.topic:
        print("Downloading core data")
    elif 'metadata' in msg.topic:
        print("Downloading metadata")
    else:
        print(f"Not downloading data with topic {msg.topic}")
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
        print(f"Saving to {temp.name}")
        with open(temp.name, "wb") as fh:
            fh.write(response.data)
        print("Data written, now putting to minio")
        # connect to MinIO
        try:
            minio_client = Minio(MINIO_HOST, access_key=MINIO_KEY,
                           secret_key=MINIO_SECRET, secure=False)
        except Exception as e:
            print("Error connecting to Minio")
            print(e)

        print("Minio connected")

        if minio_client.bucket_exists("cache"):
            print("Bucket exists")
        else:
            try:
                minio_client.make_bucket("cache")
            except Exception as e:
                print("Error creating bucket")

        # now put object
        print("Putting object")
        try:
            minio_client.fput_object("cache", f"{p}/{filename}", temp.name)
        except Exception as e:
            print("Error putting object")

        print("updating payload")
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

        pub.single(
            topic = topic,
            payload = json.dumps(payload),
            hostname = GB_HOST,
            auth={"username": GB_UID, "password": GB_PWD}
        )


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
    try:
        client.connect(host=host, port=port)
    except Exception as e:
        msg = f'failed to connect to host={host}'
        LOGGER.error(msg)
        return
    print(f"Connected to host={host}")
    with open(f"{host}.log", "w") as fh:
        fh.write("connected")

    try:
        client.loop_forever()
    except Exception as e:
        msg = f'failed to run loop_forever on host={host}'
        LOGGER.error(e)

# Load configurations
idx = 0
with open("wis2nodes.json") as fh:
    brokers = json.load(fh)

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
        if os.path.exists("sub.lock"):
            continue
        else:
            running = False

    for client in clients:
        client.disconnect()


    for t in conn_threads:
        if t is not None:
            t.join()
