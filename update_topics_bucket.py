import markdown
import glob
from minio import Minio
from dotenv import load_dotenv
load_dotenv()

import os
minio_url = os.getenv("MINIO_URL")
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

bucket = 'topics'
local_path = 'topics/*/*.md'

filepaths = glob.glob(local_path)
if len(filepaths) == 0:
    print(f'No files found for pattern={local_path}')

index_filepath = 'topics/index.html'
index_file = open(index_filepath,'w')
index_file.write('<h1>Topics</h1>\n')
# loop over files in ../topics
for filepath in filepaths:
    with open(filepath, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
        html = html.replace('<code>','<code style="white-space:pre">')
    html_filepath = filepath.replace('.md','.html')
    with open(html_filepath, 'w') as f:
        f.write(html)
    delim = '/'
    if '\\' in html_filepath:
        delim = '\\'
    topic_url = html_filepath.replace(f'topics{delim}','').replace('\\','/')
    topic_title = topic_url.split(delim)[0]
    index_file.write(f'<a href="{topic_url}">{topic_title}</a></br>\n')
    print(f'{html_filepath} created')
    content_type = 'text/html'
    client.fput_object(bucket, topic_url, html_filepath, content_type)
    print(f'Success! File available at: {protocol}{endpoint}/{bucket}/{topic_url}')
index_file.close()

client.fput_object(bucket, 'index.html', index_filepath, content_type)
print(f'Success! File available at: {protocol}{endpoint}/{bucket}/index.html')