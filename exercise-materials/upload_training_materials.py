import sys
import glob
import os

from minio import Minio
from dotenv import load_dotenv
load_dotenv()

local_path = sys.argv[1]
minio_url = os.getenv("MINIO_URL")

# hardcoded bucket-name
bucket = 'exercise-materials'

filepaths = glob.glob(local_path)
if len(filepaths) == 0:
    print(f'No files found for pattern={local_path}')

protocol = 'https://'
if minio_url.startswith('https://'):
    is_secure = True
    minio_url = minio_url.replace('https://', '')
else:
    protocol = 'http://'
    is_secure = False
    minio_url = minio_url.replace('http://', '')
creds = minio_url.split('@')[0]
endpoint = minio_url.split('@')[1].split('/')[0]
    
client = Minio(
    endpoint=endpoint,
    access_key=creds.split(':')[0],
    secret_key=creds.split(':')[1],
    secure=is_secure)

for filepath in filepaths:
    filepath = filepath.replace('\\', '/')
    identifier = filepath
    print(f"Put into bucket={bucket} : {filepath} ")
    try:
        content_type = 'application/octet-stream'
        if filepath[-4:] == 'html':
            content_type = 'text/html'
        client.fput_object(bucket, identifier, filepath, content_type)
        print(f'Success! File available at: {protocol}{endpoint}/{bucket}/{identifier}')
    except Exception as e:
        print('failed with error:')
        print(e)
