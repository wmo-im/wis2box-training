from minio import Minio

local_file = '../test-data/observations/malawi/WIGOS_0-454-2-AWSMULANJE_2023-03-14T0655.csv'
minio_path = 'mwi/malawi_wmo_demo/data/core/weather/surface-based-observations/synop/'

STORAGE_ENDPOINT = 'http://127.0.0.1:9000'
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
    STORAGE_ENDPOINT=STORAGE_ENDPOINT,
    access_key=STORAGE_USER,
    secret_key=STORAGE_PASSWORD,
    secure=is_secure)
identifier = minio_path+'/'+local_file.split('/')[-1]
print(f"Put into {BUCKET_INCOMING} : {local_file} as {identifier}")
client.fput_object(BUCKET_INCOMING, identifier, local_file)

