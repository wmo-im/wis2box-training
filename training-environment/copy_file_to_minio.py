import sys
import glob

from minio import Minio

local_path = sys.argv[1]
minio_url = sys.argv[2]

filepaths = glob.glob(local_path)
if len(filepaths) == 0:
    print(f'No files found for pattern={local_path}')

if minio_url != '' and '@' in minio_url:
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
    bucket = minio_url.split('@')[1].split('/')[1]
    minio_path = '/'
    # path is remaining bit after the bucket ...
    if len(minio_url.split('@')[1].split('/'))>2:
        minio_path = minio_url.replace(f'{creds}@{endpoint}/{bucket}','')
    client = Minio(
        endpoint=endpoint,
        access_key=creds.split(':')[0],
        secret_key=creds.split(':')[1],
        secure=is_secure)
    for filepath in filepaths:
        filepath = filepath.replace('\\', '/')
        identifier = minio_path+'/'+filepath.split('/')[-1]
        print(f"Put into {bucket} : {filepath} as {protocol}{endpoint}/{bucket}{identifier}")
    try:
        client.fput_object(bucket, identifier, filepath)
        print('succeeded')
    except Exception as e:
        print('failed with error:')
        print(e)
else:
    print('Please specify minio_url in the form http://username:password@localhost/bucket/directory')