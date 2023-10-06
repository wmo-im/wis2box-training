from minio import Minio

# replace with location of your data
local_file = 'bufr-example.bin'
# define path tp match desired topic-hierarchy for your data
minio_path = 'xyz/test/data/core/weather/surface-based-observations/synop'

# replace with your host
STORAGE_ENDPOINT = 'http://<your-host>:9000'
# your MinIO storage credentials
STORAGE_USER = 'wis2box'
STORAGE_PASSWORD = 'changetoyourpassword'

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