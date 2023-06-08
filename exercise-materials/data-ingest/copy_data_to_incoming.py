from minio import Minio

# replace with location of your data
local_file = 'myobservationdata.csv'
# define path tp match desired topic-hierarchy for your data
minio_path = 'test/data/'

# replace with your host
STORAGE_ENDPOINT = 'http://<your-host>:9000'
# your MinIO storage credentials
STORAGE_USER = 'minio'
STORAGE_PASSWORD = 'minio123'

BUCKET_INCOMING = 'wis2box-incoming'
if STORAGE_ENDPOINT.startswith('https://'):
    is_secure = True
    STORAGE_ENDPOINT = STORAGE_ENDPOINT.replace('https://', '')
else:
    is_secure = False
    STORAGE_ENDPOINT = STORAGE_ENDPOINT.replace('http://', '')

client = Minio(
    endpoint=STORAGE_ENDPOINT,
    access_key=STORAGE_USER,
    secret_key=STORAGE_PASSWORD,
    secure=is_secure)
identifier = minio_path+local_file.split('/')[-1]
print(f"Put into {BUCKET_INCOMING} : {local_file} as {identifier}")
client.fput_object(BUCKET_INCOMING, identifier, local_file)